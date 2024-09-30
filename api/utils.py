# api/utils.py

import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from .data import PRENDAS_INFO
import numpy as np
from PIL import Image, ImageEnhance
from collections import Counter
import matplotlib.pyplot as plt
import requests
from openai import OpenAI
import openai
from keys import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, OPENAI_API_KEY

# Cargar el modelo pre-entrenado de TensorFlow
model = MobileNetV2(weights='imagenet')
modelo_parte_cuerpo = MobileNetV2(weights='imagenet')


def detectar_caracteristicas(imagen):

    # Aplicar saturación
    enhancer = ImageEnhance.Color(imagen)
    img_saturated = enhancer.enhance(2.0)  # El valor 2.0 duplica la saturación, ajústalo según sea necesario
    
    # Redimensionar y preprocesar la imagen
    img = imagen.resize((224, 224))  # Cambiar el tamaño de la imagen
    img_array = np.array(img)  # Convertir la imagen a un arreglo de numpy
    img_array = np.expand_dims(img_array, axis=0)  # Añadir una dimensión para el batch
    img_array = preprocess_input(img_array)  # Preprocesar según MobileNetV2

    # Realizar la predicción
    preds = model.predict(img_array)
    decoded_preds = decode_predictions(preds, top=3)[0]

    # Extraer la información que nos interesa
    tipo_prenda = decoded_preds[0][1]  # Tipo de prenda identificado
    probabilidad = decoded_preds[0][2]  # Probabilidad de la predicción

    # Detección básica del color (promediamos los colores)
    img_np = np.array(img_saturated)

    img_np = img_np.reshape((-1, 3))  # Convertir a una lista de píxeles

    # Filtrar los píxeles no blancos
    colores_filtrados = [c for c in img_np if not (c[0] > 170 and c[1] > 170 and c[2] > 170)]  # Filtrar blanco

    # Contar la frecuencia de cada color
    contador_colores = Counter(tuple(c) for c in colores_filtrados)

    # Obtener el color más común
    color_predominante = contador_colores.most_common(1)[0][0] if contador_colores else (0, 0, 0)

    #Realizar la predicción de la parte del cuerpo
    preds_parte_cuerpo = modelo_parte_cuerpo.predict(img_array)
    decoded_preds_parte_cuerpo = decode_predictions(preds_parte_cuerpo, top=3)[0]
    
    # Obtener la parte del cuerpo identificado    
    info = obtener_info(tipo_prenda)

    return {
        'tipo_prenda': tipo_prenda,
        'probabilidad': probabilidad,
        'color': color_predominante,
        'parte_cuerpo': info.get('parte_cuerpo', 'desconocido'),
        'clima': info.get('clima_optimo', 'desconocido'),
        'nombre_es': info.get('nombre_es', 'desconocido'),
        'etiquetas': info.get('etiquetas', ['desconocido']),
    }

def filtrar_fondo_blanco(imagen_path):
    # Cargar la imagen usando OpenCV
    img = cv2.imread(imagen_path)
    
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un umbral para segmentar el fondo blanco
    _, umbral = cv2.threshold(gris, 240, 255, cv2.THRESH_BINARY)  # Ajusta el valor 240 según sea necesario

    # Invertir la máscara (0 para blanco, 255 para otros colores)
    mascara = cv2.bitwise_not(umbral)

    # Aplicar la máscara a la imagen original
    img_filtrada = cv2.bitwise_and(img, img, mask=mascara)

    # Convertir a RGB y luego a PIL para análisis
    img_pil = Image.fromarray(cv2.cvtColor(img_filtrada, cv2.COLOR_BGR2RGB))
    return img_pil

def obtener_info(tipo_prenda):
    info = PRENDAS_INFO.get(tipo_prenda.lower())
    if info:
        return info
    else:
        return {
            "parte_cuerpo": "desconocido",
            "clima_optimo": "desconocido",
            "nombre_es": "desconocido",
            "etiquetas": ["desconocido"]
        }

def obtener_datos_climaticos(lat, lon):
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': OPENWEATHER_API_KEY,
            'exclude': 'minutely,hourly',  
            'units': 'metric',            
            'lang': 'es'                   
        }

        response = requests.get(OPENWEATHER_BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            return {
                'current_weather': data.get('current', {}),
                'daily_forecast': data.get('daily', []),
                'alerts': data.get('alerts', [])
            }
        else:
            return {'error': f'Error fetching weather data: {response.status_code}'}

    except requests.RequestException as e:
        return {'error': str(e)}

def consultar_chat_gpt(prompt):

    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
            "content": prompt,
            "max_tokens": 150,
            "temperature": 0.7,
            "top_p": 1.0,            
            },
        ],
    )

    return response.choices[0].message.content


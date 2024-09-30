from django.shortcuts import render
from django.http import JsonResponse
from .models import Prenda, Combinacion
from .serializers import PrendaSerializer, CombinacionSerializer, ImagenPrendaSerializer
from .utils import detectar_caracteristicas, obtener_datos_climaticos, consultar_chat_gpt
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from PIL import Image
import io



# Create your views here.


#This imprts the Prenda model from the models.py file
class PrendaListCreate(generics.ListCreateAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer

class CombinacionListCreate(generics.ListCreateAPIView):
    queryset = Combinacion.objects.all()
    serializer_class = CombinacionSerializer

class PrendasRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer
    lookup_field = 'id'

class CombinacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prenda.objects.all()
    serializer_class = CombinacionSerializer
    lookup_field = 'id'



class ProcesarImagenView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImagenPrendaSerializer(data=request.data)
        if serializer.is_valid():
            imagen = serializer.validated_data['imagen']

            # Abrir la imagen directamente desde el objeto InMemoryUploadedFile
            try:
                img = Image.open(imagen)  # Usar PIL para abrir la imagen
                
                # Llamar a la función de detección de características
                resultado = detectar_caracteristicas(img)  # Pasar el objeto de imagen directamente

                return Response(resultado, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeatherAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Extract latitude and longitude from query parameters
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')

        if not lat or not lon:
            lat=4.60971
            lon=-74.08175
            #return Response({'error': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch weather data
        weather_data = obtener_datos_climaticos(lat, lon)

        return Response(weather_data, status=status.HTTP_200_OK if 'error' not in weather_data else status.HTTP_400_BAD_REQUEST)

class ConsultarChatGPTView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        prompt = request.data.get("prompt", "")

        if not prompt:
            return Response(
                {"error": "Debe proporcionar un prompt para la consulta"},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json"
            )

        # Llamar a la función que hace la consulta a OpenAI
        resultado = consultar_chat_gpt(prompt)

        return Response({"respuesta": resultado}, status=status.HTTP_200_OK)


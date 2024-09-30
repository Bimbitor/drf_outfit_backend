from rest_framework import serializers
from .models import Prenda, Combinacion


class PrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prenda
        fields = '__all__'

class CombinacionSerializer(serializers.ModelSerializer):
    prendas = PrendaSerializer(many=True)  # Permitirá incluir prendas en el registro de combinaciones

    class Meta:
        model = Combinacion
        fields = '__all__'

    def crear(self, validated_data):
        prendas_data = validated_data.pop('prendas')
        Combinacion = Combinacion.objects.create(**validated_data)
        for clothe_data in prendas_data:
            clothe, _ = Clothe.objects.get_or_create(**clothe_data)
            Combinacion.prendas.add(clothe)
        return Combinacion

class ImagenPrendaSerializer(serializers.Serializer):
    imagen = serializers.ImageField()



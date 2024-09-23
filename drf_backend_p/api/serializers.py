from rest_framework import serializers
from .models import Prenda, Combinacion, PrendasCombinacion


class PrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prenda
        fields = '__all__'

class CombinacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combinacion
        fields = '__all__'

class PrendasCombinacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrendasCombinacion
        fields = '__all__'

from django.shortcuts import render
from rest_framework import generics
from .models import Prenda, Combinacion, PrendasCombinacion
from .serializers import PrendaSerializer, CombinacionSerializer, PrendasCombinacionSerializer

# Create your views here.


#This imprts the Prenda model from the models.py file
class PrendaListCreate(generics.ListCreateAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer

class CombinacionListCreate(generics.ListCreateAPIView):
    queryset = Combinacion.objects.all()
    serializer_class = CombinacionSerializer

class PrendasCombinacionListCreate(generics.ListCreateAPIView):
    queryset = PrendasCombinacion.objects.all()
    serializer_class = PrendasCombinacionSerializer

class PrendasRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer
    lookup_field = 'id'

class CombinacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prenda.objects.all()
    serializer_class = CombinacionSerializer
    lookup_field = 'id'

class PrendasCombinacionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendasCombinacionSerializer
    lookup_field = 'id'
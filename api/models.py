from django.db import models


class Prenda(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activa'),
        ('I', 'Inactiva'),
    ]

    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='clothes/')
    tipo = models.CharField(max_length=50)
    color = models.CharField(max_length=50, null=True, blank=True)
    talla = models.CharField(max_length=20, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True)
    clima = models.CharField(max_length=50, null=True, blank=True)
    parte_cuerpo = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Combinacion(models.Model):
    CATEGORIA_CHOICES = [
        ('formal', 'Formal'),
        ('casual', 'Casual'),
        ('sport', 'Sport'),
    ]

    CLIMA_CHOICES = [
        ('caluroso', 'Caluroso'),
        ('frío', 'Frío'),
        ('templado', 'Templado'),
    ]

    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    clima = models.CharField(max_length=50, choices=CLIMA_CHOICES)
    fecha_programacion = models.DateField(unique=True)
    estado = models.CharField(max_length=1, choices=Prenda.ESTADO_CHOICES, default='A')
    Prendas = models.ManyToManyField(Prenda, related_name='combinaciones')

    def __str__(self):
        return f"Combinación {self.categoria} - {self.fecha_programacion}"



from django.db import models


# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=60, primary_key=True)


class Producto(models.Model):
    nombre = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    unidades = models.IntegerField()
    precio = models.FloatField();
    detalles = models.CharField(max_length=100)
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)

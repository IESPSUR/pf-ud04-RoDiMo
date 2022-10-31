from django.db import models


# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=60, primary_key=True)


class Producto(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    modelo = models.CharField(max_length=60, unique=True)
    unidades = models.IntegerField()
    precio = models.FloatField();
    detalles = models.CharField(max_length=100)
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)


class Compra(models.Model):
    fecha = models.DateTimeField()
    importe = models.FloatField()
    unidades = models.IntegerField()
    nombre = models.ForeignKey('Producto', to_field='nombre', related_name='Nombre', on_delete=models.CASCADE)
    modelo = models.ForeignKey('Producto', to_field='modelo', related_name='Modelo', on_delete=models.CASCADE)



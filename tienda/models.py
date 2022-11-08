from django.db import models
from django.forms import ModelForm


# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=60, primary_key=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    modelo = models.CharField(max_length=60)
    unidades = models.IntegerField()
    precio = models.FloatField()
    detalles = models.CharField(max_length=100)
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    fecha = models.DateTimeField()
    importe = models.FloatField()
    unidades = models.IntegerField()
    nombre = models.ForeignKey('Producto', on_delete=models.CASCADE)


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class CheckoutForm(ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'

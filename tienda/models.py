from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django import forms
from django.shortcuts import get_object_or_404


# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=60, primary_key=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    unidades = models.IntegerField()
    precio = models.FloatField()
    detalles = models.CharField(max_length=100)
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Compra(models.Model):
    fecha = models.DateTimeField()
    importe = models.FloatField()
    unidades = models.IntegerField()
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class CheckoutForm(forms.Form):
    unidades = forms.FloatField(label='unidades')




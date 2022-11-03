from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    producto = Producto.objects.all()

    return render(request, 'tienda/listado.html', {'producto': producto})


def nuevo_prod(request):
    form = ProductoForm()
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = Producto()

            producto.nombre = form.cleaned_data['nombre']
            producto.modelo = form.cleaned_data['modelo']
            producto.unidades = form.cleaned_data['unidades']
            producto.precio = form.cleaned_data['precio']
            producto.precio = form.cleaned_data['precio']
            producto.d = form.cleaned_data['precio']
            producto.marca = form.cleaned_data['marca']

            producto.save()
        else:
            print("Formulario invalido")
    return render(request, 'tienda/nuevo.html', {'form': form})



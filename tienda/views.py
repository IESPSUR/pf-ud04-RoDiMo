from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import *


# Create your views here.

# CRUD
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
            producto.detalles = form.cleaned_data['detalles']
            producto.marca = form.cleaned_data['marca']

            producto.save()
        else:
            print("Formulario invalido")
    return render(request, 'tienda/nuevo.html', {'form': form})


def actualizar_prod(request, pk):
    producto = get_object_or_404(Producto, id=pk)

    form = ProductoForm(instance=producto)
    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():

            producto.nombre = form.cleaned_data['nombre']
            producto.modelo = form.cleaned_data['modelo']
            producto.unidades = form.cleaned_data['unidades']
            producto.precio = form.cleaned_data['precio']
            producto.detalles = form.cleaned_data['detalles']
            producto.marca = form.cleaned_data['marca']

            producto.save()
        else:
            print("Formulario invalido")

    return render(request, 'tienda/actualizar.html', {'form': form})


def eliminar_prod(request, pk):
    producto = get_object_or_404(Producto, id=pk)

    if request.method == "POST":
        producto.delete()
        return redirect('listado')
    contexto = {
        "prod": producto
    }
    return render(request, 'tienda/cofirmar_borrado.html', contexto)


# Proceso de Compra
def listado_compra(request):
    producto = Producto.objects.all()

    return render(request, 'tienda/listado_compra.html', {'producto': producto})


def checkout(request, pk):
    compra = get_object_or_404(Compra, id=pk)
    form = CheckoutForm(instance=compra)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():

            compra.nombre = form.cleaned_data['nombre']
            compra.unidades = form.cleaned_data['unidades']
            compra.importe = form.cleaned_data['importe']
            compra.fecha = datetime.now()
    return render(request, 'tienda/checkout.html', {'form': form})

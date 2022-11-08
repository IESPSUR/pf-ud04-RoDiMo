from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import request
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

    return render(request, 'tienda/cofirmar_borrado.html', {"prod": producto})


# Proceso de Compra

# Lista y búsqueda de productos
def listado_compra(request):
    busqueda = request.POST.get('buscar', '')
    producto = Producto.objects.all()

    # Filtro los productos por nombre y por marca
    if busqueda:
        producto = Producto.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(marca__nombre__icontains=busqueda)
        ).distinct()

    return render(request, 'tienda/listado_compra.html', {'producto': producto})


# Checkout
def checkout(request, pk):
    form = CheckoutForm()
    producto = Producto.objects.all()
    p = get_object_or_404(Producto, id=pk)
    # Comprueba que el numero de unidades introducidas sea menor
    # a las que hay en la base de datos.(Este valor se pasará al template)
    validacion_unidades = True;

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Obtengo las unidades del formulario
            unidades = form.cleaned_data['unidades']

            # Compruebo la cantidad de unidades
            if unidades > p.unidades:
                validacion_unidades = False
            else:
                p.unidades = p.unidades - unidades
                p.save()
            return render(request, 'tienda/checkout.html', {'form': form, 'unidades': unidades, 'producto': producto,
                                                            'pk': pk, 'validacion_unidades': validacion_unidades})
    else:
        return render(request, 'tienda/checkout.html', {'form': form, 'producto': producto, 'pk': pk})

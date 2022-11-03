from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    producto = Producto.objects.all()

    return render(request, 'tienda/listado.html', {'producto': producto})



from _ast import Mult
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, Sum
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


# Create your views here.

# CRUD
def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    producto = Producto.objects.all()
    listaproducto = list(producto)

    return render(request, 'tienda/listado.html', {'listaproducto': listaproducto})


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

# Lista y b??squeda de productos
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
@transaction.atomic
def checkout(request, pk):
    form = CheckoutForm()

    p = get_object_or_404(Producto, id=pk)

    # Comprueba que el numero de unidades introducidas sea menor
    # a las que hay en la base de datos.(Este valor se pasar?? al template)
    validacion_unidades = True;

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Obtengo las unidades del formulario
            unidades = form.cleaned_data['unidades']

            # Obtener id del usuario
            if request.user.is_authenticated:
                usuario = request.user.id

            else:
                usuario = None

            # Compruebo la cantidad de unidades
            if unidades > p.unidades:
                mensaje = messages.add_message(request, messages.INFO, f"El numero de unidades excede a las disponibles .")
                return redirect('checkout', pk )
            else:
                p.unidades = p.unidades - unidades
                p.save()

                # A??adir la informacion a Compras

                Compra.objects.create(fecha=timezone.now(), importe=p.precio * unidades, unidades=unidades, producto=p,
                                      usuario_id=usuario)

            return redirect("listado_compra")
    else:
        return render(request, 'tienda/checkout.html', {'form': form, 'producto': p, 'pk': pk})


######## Informes ##########

def informe(request):
    return render(request, 'tienda/informe.html', {})


def informes_marca(request):
    marcas = Marca.objects.all().values()
    lista = list(marcas)

    return render(request, 'tienda/listado_informes.html', {'lista': lista})


def marcas_detalles(request, nombre):
    listaproducto = Producto.objects.filter(marca__nombre__icontains=nombre).values()
    return render(request, 'tienda/listado.html', {'listaproducto': listaproducto})


def top_productos(request):
    productos = Compra.objects.values('producto__nombre').annotate(unidades_vendidas=Sum('unidades')).order_by(
        '-unidades_vendidas')[:10]
    productos = list(productos)

    return render(request, 'tienda/top_productos.html', {'productos': productos})


def top_usuarios(request):
    usuarios = User.objects.values('username').annotate(importe_compras=Sum('compra__importe')).order_by(
        '-importe_compras')[:10]

    return render(request, 'tienda/top_usuarios.html', {'usuarios': usuarios})


def informes_usuario(request):
    compras = User.objects.all().values()
    lista = list(compras)

    return render(request, 'tienda/listado_usuarios.html', {'lista': lista})


def usuarios_detalles(request, usuario):
    listaproducto = Compra.objects.filter(usuario=usuario).values()
    user = User.objects.values('username').filter(id=usuario)
    return render(request, 'tienda/usuarios_compras.html', {'listaproducto': listaproducto, 'usuario': user})


#### Registrar, logear y desogear usuarios #####

def registro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            us = form.save()
            login(request, us)
            messages.success(request, "Registro exitoso")
            return redirect('welcome')
        messages.add_message(request,messages.INFO, "Registro invalido. Informaci??n erronea")
    form = UserCreationForm()
    return render(request, "tienda/registro.html", {"formulario_registro": form})


def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, f"Estas conectdo como {username}.")
            else:
                messages.add_message(request, messages.INFO, f"Nombre de usuario o contrase??a invalido")

        else:
            messages.add_message(request,messages.INFO, f"Nombre de usuario o contrase??a invalido")
    form = AuthenticationForm()
    return render(request, 'tienda/login.html', {'formulario_login': form})


def logout_usuario(request):
    logout(request)
    messages.info(request, "Se ha deslogeado satisfactoriamente")
    return redirect('welcome')

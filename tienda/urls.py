from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/listado', views.listado, name='listado'),
    path('tienda/admin/nuevo', views.nuevo_prod, name='nuevo'),

]

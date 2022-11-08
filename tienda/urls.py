from django.urls import path
from . import views

urlpatterns = [
    # CRUD

    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/listado', views.listado, name='listado'),
    path('tienda/admin/nuevo', views.nuevo_prod, name='nuevo'),
    path('tienda/admin/update/<int:pk>', views.actualizar_prod, name='update'),
    path('tienda/admin/delete/<int:pk>', views.eliminar_prod, name='delete'),

    # Compra
    path('tienda/compra', views.listado_compra, name='listado_compra'),
    path('tienda/checkout/<int:pk>', views.checkout, name='checkout'),
]

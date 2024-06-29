from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('carrito', views.carrito, name='carrito'),
    path('pagina_producto/<int:id>', views.paginaProducto, name='paginaProducto'),
    path('catalogo', views.catalogo, name='catalogo'),
]

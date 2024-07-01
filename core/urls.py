from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('carrito', views.carrito, name='carrito'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('pagina_producto/<int:id>', views.paginaProducto, name='paginaProducto'),
    path('catalogo', views.catalogo, name='catalogo'),
    path('registro', views.registroUsuario, name='registroUsuario'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('acceso_usuario', views.acceso_usuario, name='acceso_usuario'),
    path('formularioContacto', views.formularioContacto, name='formularioContacto'),
    path('vendedor/home', views.v_home, name='v_home' ),
    path('vendedor/registroVehiculo',views.v_registroVehiculo, name='registroVehiculo'),
    path('vendedor/modificarProducto/',views.modificarProducto, name='v_modificarProducto' ),
    path('vendedor/paginaProducto/<int:id>',views.v_paginaProducto, name='v_paginaProducto' ),
    path('vendedor/eliminarProducto/<int:id>',views.v_eliminarProducto, name = 'v_eliminarProducto' ),
]
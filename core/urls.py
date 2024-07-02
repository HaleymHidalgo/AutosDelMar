from django.urls import path
from . import views

urlpatterns = [
    #----- Cliente -----
    path('', views.home, name='home'),
    path('carrito/', views.carrito, name='carrito'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('pagina_vehiculo/<int:id>', views.paginaVehiculo, name='paginaVehiculo'),
    path('pagina_accesorio/<int:id>', views.paginaAccesorio, name='paginaAccesorio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('registro/', views.registroUsuario, name='registroUsuario'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('acceso_usuario/', views.acceso_usuario, name='acceso_usuario'),
    path('formularioContacto/', views.formularioContacto, name='formularioContacto'),
    #------- Vendedor -----
    path('vendedor/home', views.v_home, name='v_home' ),
    path('vendedor/eliminarProducto/<int:id>',views.v_eliminarProducto, name = 'v_eliminarProducto' ),
    #------- Vehiculo -----
    path('vendedor/registroVehiculo',views.v_registroVehiculo, name='registroVehiculo'),
    path('vendedor/modificarProducto/',views.modificarProducto, name='v_modificarVehiculo' ),
    path('vendedor/pagina_vehiculo/<int:id>',views.v_paginaVehiculo, name='v_paginaVehiculo' ),
    #-------- Accesorio -----
    path('vendedor/pagina_accesorio/<int:id>',views.v_paginaAccesorio, name='v_paginaAccesorio' ),
    path('vendedor/modificarAccesorio/',views.modificarAccesorio, name='v_modificarAccesorio' ),
    path('vendedor/registroAccesorio/', views.registroAccesorio, name='registroAccesorio'),
]
from django.shortcuts import render
from . import models

# Create your views here.
def home(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {
            'vehiculos': vehiculos
        }
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'home.html', context)

def carrito(request):
    return render(request, 'carrito.html')

def nosotros(request):
    return render(request, 'nosotros.html')
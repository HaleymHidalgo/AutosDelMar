from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {'vehiculos': vehiculos}
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'home.html', context)

@login_required(login_url='home')
def carrito(request):
    return render(request, 'carrito.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def paginaProducto(request, id):
    #Aqui nosotros obtenemos el producto que queremos mostrar
    vehiculo = models.Vehiculo.objects.get(producto_id=id)
    context = {
        'vehiculo': vehiculo,
        'formulario': forms.formularioContacto
    }
    return render(request, 'paginaProducto.html', context)

def catalogo(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {'vehiculos': vehiculos}
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'catalogo.html', context)
    
def registroUsuario(request):
    if request.method == 'POST':
        form = forms.registroUsuario(request.POST)
        print(form)
        if form.is_valid():
            
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
        else:
            return render(request, 'acceso/registro.html', {'form': form, 'error': 'Datos invalidos'})
    return render(request, 'acceso/registro.html', {'form': forms.registroUsuario})

def acceso_usuario(request):
    if request.method == 'POST':
        form = forms.accesoUsuario(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            usuario = authenticate(request,
                        username=clean_data['usuario_id'],
                        password=clean_data['password']
                    )
            if (usuario is not None):
                if usuario.is_active:
                    login(request, usuario)
                    return redirect('home')
                else:
                    return render(request, 'acceso/acceso.html', {
                        'form': forms.accesoUsuario,
                        'error': 'El usuario no esta activo'
                    })
            else:
                return render(request, 'acceso/acceso.html', {
                    'form': forms.accesoUsuario,
                    'error': 'El usuario no existe'
                })
        else:
            return render(request, 'acceso/acceso.html', {
                'form': forms.accesoUsuario,
                'error': 'Datos invalidos'
            })
    else:
        return render(request, 'acceso/acceso.html', {'form': forms.accesoUsuario})

def formularioContacto (request):
    if request.method == 'POST':
        form = forms.formularioContacto(request.POST)
        contacto = models.Contacto.objects.create(
            nombre = request.POST['nombre'],
            apellido = request.POST['apellido'],
            telefono = request.POST['telefono'],
            correo = request.POST['correo']
        )
        try:
            if contacto.save():
                return redirect('home')
            else:
                raise Exception('No se pudo guardar el contacto')
        except:
            return render(request, 'paginaProducto.html', {'form': forms.formularioContacto, 'error': 'Datos invalidos'})  
        
    else:
        return render(request, 'paginaProducto.html', {'form': forms.formularioContacto})

#Funcion para deslogear al usuario
def cerrar_sesion(request):
    logout(request)
    return redirect('home')
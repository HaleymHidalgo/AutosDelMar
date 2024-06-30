from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import ssl
import smtplib
from email.message import EmailMessage
from django.conf import settings

# Create your views here.
def home(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {
            'vehiculos': vehiculos,
            'MEDIA_URL': settings.MEDIA_URL
            }
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
#funcion enviar correo
def enviarCorreo(contacto):
    print ("esta wea esta funcionando")
    Email = 'autosdelmar.project@gmail.com'
    #no es la contrase;a del correo te lo proporciona google mediante este link myaccount.google.com/u/1/apppasswords
    contraseña = 'ynms qvch shzj yfhd'
    To = contacto.correo
    print (contacto.correo)
    Subject = 'Cita confirmada'
    Body = """
    Su cita a sido confirmada lo llamaremos para mas informacion.
    """

    # Crear objeto de mail
    em = EmailMessage()
    em['From'] = Email
    em['To'] = To
    em['Subject'] = Subject
    em.set_content(Body)

    # Añadir SSL (extra de seguridad)
    context = ssl.create_default_context()

    # Iniciar sesión y enviar el mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(Email, contraseña)
        smtp.sendmail(Email, To, em.as_string())

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
            contacto.save()
            enviarCorreo(contacto)
            return redirect('home')
            
                
        except:
            return render(request, 'paginaProducto.html', {'form': forms.formularioContacto, 'error': 'Datos invalidos'})  
        
    else:
        return render(request, 'paginaProducto.html', {'form': forms.formularioContacto})

#carrito
    productos = {  }
    for producto in 50:
        producto.append(producto)

    context = {
        'productos': productos
    }   

    productos = Producto.objects.all()
    total = sum(producto.precio for producto in productos)
    context = {
        'productos': productos,
        'total': total,
    }
    return render(request, 'carrito.html', context)
#vendedor
def v_home(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {'vehiculos': vehiculos}
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'vendedor/home.html', context)
    
def v_registroVehiculo(request):
    if request.method == 'POST':
        form = forms.registroVehiculo(request.POST,request.FILES)
        if form.is_valid():
            producto = models.Producto.objects.create(
                    precio = form.cleaned_data['precio'],
                    descripcion = form.cleaned_data['descripcion'],
                    cantidad = form.cleaned_data['cantidad'],
                    image = form.cleaned_data['image'])
            producto.save()
            vehiculo = models.Vehiculo.objects.create(
                    producto_id=producto,
                    marca=form.cleaned_data['marca'],
                    modelo=form.cleaned_data['modelo'],
                    carroceria=form.cleaned_data['carroceria'],
                    anio=form.cleaned_data['anio'],
                    combustible=form.cleaned_data['combustible'],
                    transmision=form.cleaned_data['transmision']
                )
            try:
                producto.save()
                vehiculo.save()
                return redirect('v_home')
            except Exception as e:
                print(f'Error al crear producto: {e}')
                return render(request, 'vendedor/registroVehiculo.html', {'form': form, 'error': 'Error al crear el producto'})
    return render(request, 'vendedor/registroVehiculo.html', {'form': forms.registroVehiculo})

#Funcion para deslogear al usuario
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

#funcion enviar correo

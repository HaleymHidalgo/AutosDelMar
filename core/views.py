from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
import ssl
import smtplib
from email.message import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from PIL import Image
import os
from datetime import datetime

# Create your views here.
def home(request):
    if request.method == 'GET':
        #Validamos si el usuario esta autenticado
        if(request.user.is_authenticated):
            #Si lo esta, verificamos si el usuario es un vendedor
            try:
                grupos = request.user.groups.values_list('name', flat=True)
                if list(grupos)[0] == 'vendedor':
                    return redirect('v_home')
            except Exception as e:
                print(f"Error: {str(e)}")
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {
            'vehiculos': vehiculos,
            'MEDIA_URL': settings.MEDIA_URL
            }
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'home.html', context)

@login_required(login_url='acceso_usuario')
def carrito(request):
    return render(request, 'carrito.html')

def nosotros(request):
    if(request.user.is_authenticated):
            grupos = request.user.groups.values_list('name', flat=True)
            if list(grupos)[0] == 'vendedor':
                return redirect('v_home')
    return render(request, 'nosotros.html')

def paginaProducto(request, id):
    if(request.user.is_authenticated):
            grupos = request.user.groups.values_list('name', flat=True)
            if list(grupos)[0] == 'vendedor':
                return redirect('v_home')
    #Aqui nosotros obtenemos el producto que queremos mostrar
    vehiculo = models.Vehiculo.objects.get(producto_id=id)
    context = {
        'vehiculo': vehiculo,
        'formulario': forms.formularioContacto
    }
    return render(request, 'paginaProducto.html', context)

def catalogo(request):
    if request.method == 'GET':
        if(request.user.is_authenticated):
            grupos = request.user.groups.values_list('name', flat=True)
            if list(grupos)[0] == 'vendedor':
                return redirect('v_home')
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {'vehiculos': vehiculos}
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'catalogo.html', context)
    
def registroUsuario(request):
    if(request.user.is_authenticated):
        return redirect('home')
    if request.method == 'POST':
        form = forms.registroUsuario(request.POST)
        if form.is_valid():
            #Creamos una intancia del Grupo al que añadiremos al Usuario
            grupo = Group.objects.get(name='cliente')
            #Creamos el usuario con los datos del formulario y lo guardamos en una variable
            user = form.save()
            #le añadirmos el grupo al usuario
            user.groups.add(grupo)
            #Modificamos el usuario en la base de datos
            user.save()
            #Autenticamos al usuario
            login(request, user)
            #Se redirigimos al usuario a la pagina principal
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
                    #verificamos si el usuario es un vendedor
                    grupos = request.user.groups.values_list('name', flat=True)
                    return redirect('v_home') if list(grupos)[0] == 'vendedor' else redirect('home')
                
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

#vendedor
@login_required(login_url='acceso_usuario')
def v_home(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {'vehiculos': vehiculos}
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'vendedor/home.html', context)
    else:
        return redirect('home')

@login_required(login_url='acceso_usuario')
def v_registroVehiculo(request):
    if request.method == 'POST':
        try:
            #nombre Archivo (Fecha y hora de guardado)
            nameImg = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png'
            #Creamos una ruta para guardar la imagen en el servidor
            imgPath = os.path.join(settings.MEDIA_ROOT, 'db-images/vehiculos/', nameImg)
            #verifica que el directorio existe (si no existe lo crea)
            os.makedirs(os.path.dirname(imgPath), exist_ok=True)
            #Creamos una instancia de la clase Image de la libreria PIL para guardar la imagen
            img = Image.open(request.FILES['imgProducto'])
            img.save(imgPath)
            
            producto = models.Producto.objects.create(
                precio = request.POST['precio'],
                descripcion = request.POST['descripcion'],
                cantidad = request.POST['cantidad'],
                image = imgPath
            )
            #Guardamos el producto en la base de datos
            producto.save()
            
            vehiculo = models.Vehiculo.objects.create(
                        producto_id=producto,
                        marca = request.POST['marca'],
                        modelo = request.POST['modelo'],
                        carroceria = request.POST['carroceria'],
                        anio = request.POST['anio'],
                        combustible = request.POST['combustible'],
                        transmision = request.POST['transmision']
            )
            #guadamos el vehiculo en la base de datos
            vehiculo.save()
            return redirect('v_home')
            
        except Exception as e:
            print(f'Error al crear producto: {e}')
            return render(request, 'vendedor/registroVehiculo.html', {'form': forms.registroVehiculo, 'error': 'Error al crear el producto'})
    if request.method == 'GET':
        return render(request, 'vendedor/registroVehiculo.html', {'form': forms.registroVehiculo})
    else:
        #No deberia llegar aqui nadie (salvo que alguien clone la pagina)
        pass

@login_required(login_url='acceso_usuario')
def v_paginaProducto(request, id):
    #Aqui nosotros obtenemos el producto que queremos mostrar
    if request.method == 'GET':
        vehiculo = models.Vehiculo.objects.get(producto_id=id)

        llenar_datos ={
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo,
            'carroceria': vehiculo.carroceria,
            'combustible': vehiculo.combustible,
            'anio': vehiculo.anio,
            'transmision': vehiculo.transmision,
            'precio': vehiculo.producto_id.precio,
            'descripcion': vehiculo.producto_id.descripcion,
            'cantidad': vehiculo.producto_id.cantidad,
            'image': vehiculo.producto_id.image.url,
        }
        form= forms.registroVehiculo(initial=llenar_datos)
        context = {
            'vehiculo': vehiculo,
            'formulario': form,
            'titulo':'Detalles del Vehículo',
            'imagen':vehiculo.producto_id.image.url
        }
        return render(request, 'vendedor/paginaProducto.html',context)
    
def modificarProducto(request):
    #Aqui actualizaremos los datos del producto
    if request.method == 'POST':
        print('ok')
        image = Image.open(request.POST.get('image'))
        image.show()
        form = forms.registroVehiculo(request.POST,request.FILES)
        if form.is_valid():
            producto = models.Producto.objects.create(
                    precio = form.cleaned_data['precio'],
                    descripcion = form.cleaned_data['descripcion'],
                    cantidad = form.cleaned_data['cantidad'],
                    image = form.cleaned_data['image'])
            print(producto)
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
            print(vehiculo)
            vehiculo.save()
            return redirect('v_home')
        else:
            return HttpResponse('esta malo')

@login_required(login_url='acceso_usuario')
def v_eliminarProducto(request, id):
    if request.method == 'DELETE':
        try:
            producto = get_object_or_404(models.Producto, producto_id=id)
            producto.delete()
            return JsonResponse({'message': 'Vehículo eliminado con éxito'}, status=204)
        except models.Producto.DoesNotExist:
            return JsonResponse({'message': 'El vehículo no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error al eliminar el vehículo: {str(e)}'}, status=500)
    else:
        return JsonResponse('message', status=405)

#Funcion para deslogear al usuario
@login_required(login_url='acceso_usuario')
def cerrar_sesion(request):
    logout(request)
    return redirect('home')
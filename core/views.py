from django.shortcuts import get_object_or_404, redirect, render
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
from django.views.decorators.csrf import csrf_exempt

#----------------------- Cliente -----------------------
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
        vehiculos = models.Vehiculo.objects.filter(producto_id__estado_producto = True)
        accesorios = models.Accesorio.objects.filter(producto_id__estado_producto=True)
        context = {
            'vehiculos': vehiculos,
            'accesorios': accesorios
        }
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'home.html', context)

@login_required(login_url='acceso_usuario')
def carrito(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            user = request.user
            
            # Obtener o crear la orden de compra para el usuario actual
            orden, created = models.OrdenCompra.objects.get_or_create(cliente=user, completada=False)
            
            # Filtrar los detalles de la orden específica
            detalles = models.DetalleOrden.objects.filter(orden=orden)
            
            # Lista para almacenar los accesorios relacionados
            accesorios = []
            for item in detalles:
                accesorio = models.Accesorio.objects.get(producto_id=item.producto.producto_id)
                accesorios.append({
                    'idDetalle': item.pk,
                    'imagen': accesorio.producto_id.image,
                    'nombre': accesorio.nombre,
                    'precio': accesorio.producto_id.precio,
                    'cantidad': item.cantidad,
                    'subtotal': item.producto.precio * item.cantidad
                })
            
            #Falta añadir un context con los vehiculos y accesorios para recorrer
            total = sum(item.producto.precio * item.cantidad for item in detalles)
            
            context = {
                'orden': orden,
                'productos':accesorios,
                'total':total
            }
            
            return render(request, 'carrito.html', context)        
        
    redirect('home')

def nosotros(request):
    if(request.user.is_authenticated):
            grupos = request.user.groups.values_list('name', flat=True)
            if list(grupos)[0] == 'vendedor':
                return redirect('v_home')
    return render(request, 'nosotros.html')

def paginaVehiculo(request, id):
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
    return render(request, 'paginaVehiculo.html', context)

def paginaAccesorio(request, id):
    if(request.user.is_authenticated):
            grupos = request.user.groups.values_list('name', flat=True)
            if list(grupos)[0] == 'vendedor':
                return redirect('v_home')
    #Aqui nosotros obtenemos el producto que queremos mostrar
    accesorio = models.Accesorio.objects.get(producto_id=id)
    context = {
        'accesorio': accesorio,
        'formulario': forms.formularioContacto
    }
    return render(request, 'paginaAccesorio.html', context)

def catalogo(request):
    if request.method == 'GET':
        if(request.user.is_authenticated):
            grupos = request.user.groups.values_list('name', flat=True)
            if list(grupos)[0] == 'vendedor':
                return redirect('v_home')
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.filter(producto_id__estado_producto = True)
        accesorios = models.Accesorio.objects.filter(producto_id__estado_producto=True)
        context = {
            'vehiculos': vehiculos,
            'accesorios': accesorios
        }
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'catalogo.html', context)
    else:
        return HttpResponse("idkmen")
    
@csrf_exempt
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
    Subject = 'Confirmación de Cita - Autos del Mar'
    Body = f"""
Estimado/a {contacto.nombre} {contacto.apellido},

Nos complace confirmar su cita con Autos del Mar
para la reserva de un vehiculo. Le recomendamos
llegar unos minutos antes de su cita para
asegurar que podamos atenderle puntualmente.

Si tiene alguna pregunta o necesita reprogramar,
no dude en contactarnos respondiendo a este correo.

Gracias por elegir Autos del Mar. ¡Esperamos verle pronto!

Atentamente,

Autos del Mar
{Email}
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

def perfil(request):
        if request.method == 'GET':
            #Aqui nosotros obtenemos el usuario logeado
            usuario = request.user
            context = {
                'usuario': usuario
            }
            #le vamos a pasarle el contexto a la plantilla
            return render(request, 'perfil.html', context)
        else:
            return redirect('home')

#------------------------- Vendedor -------------------------
@login_required(login_url='acceso_usuario')
def v_home(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.filter(producto_id__estado_producto = True)
        accesorios = models.Accesorio.objects.filter(producto_id__estado_producto=True)
        context = {
            'vehiculos': vehiculos,
            'accesorios': accesorios
        }
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'vendedor/home.html', context)
    else:
        return redirect('home')

#----- Vehiculo ----
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
                image = settings.MEDIA_URL + 'db-images/vehiculos/' + nameImg
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
            return render(request, 'vendedor/registroProducto.html', {'form': forms.registroVehiculo, 'error': 'Error al crear el producto'})
    if request.method == 'GET':
        context = {
            'form': forms.registroVehiculo,
            'titulo': 'Vehículo',
        }
        return render(request, 'vendedor/registroVehiculo.html', context)
    else:
        #No deberia llegar aqui nadie (salvo que alguien clone la pagina)
        pass

@login_required(login_url='acceso_usuario')
def v_paginaVehiculo(request, id):
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
            'image': vehiculo.producto_id.image
        }
        form= forms.registroVehiculo(initial=llenar_datos)
        context = {
            'vehiculo': vehiculo,
            'formulario': form,
            'titulo':'Detalles del Vehículo',
            'hiddenImagen':vehiculo.producto_id.image,
            'hiddenId':vehiculo.producto_id.producto_id
        }
        return render(request, 'vendedor/paginaVehiculo.html', context)
    
def modificarProducto(request):
    #Aqui actualizaremos los datos del producto
    if request.method == 'POST':
        try:
            if 'imgProducto' in request.FILES:
                #nombre Archivo (Fecha y hora de guardado)
                nameImg = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png'
                #Creamos una ruta para guardar la imagen en el servidor
                imgPath = os.path.join(settings.MEDIA_ROOT, 'db-images/vehiculos/', nameImg)
                #verifica que el directorio existe (si no existe lo crea)
                os.makedirs(os.path.dirname(imgPath), exist_ok=True)
                #Creamos una instancia de la clase Image de la libreria PIL para guardar la imagen
                img = Image.open(request.FILES['imgProducto'])
                img.save(imgPath)
                #URL de la imagen para la base de datos
                imgURL = settings.MEDIA_URL + '/db-images/vehiculos/' + nameImg
            else:
                imgURL = request.POST['imgProductoOld']
            
            #Obtenemos los datos del producto y vehiculo de la base de datos
            producto_id = request.POST['idProducto']
            producto = models.Producto.objects.get(producto_id=producto_id)
            vehiculo = models.Vehiculo.objects.get(producto_id=producto)
            
            # Actualizamos los datos del producto
            producto.precio = request.POST['precio']
            producto.descripcion = request.POST['descripcion']
            producto.cantidad = request.POST['cantidad']
            producto.image = imgURL
            producto.save()
            
            # Actualizamos los datos del vehículo
            vehiculo.marca = request.POST['marca']
            vehiculo.modelo = request.POST['modelo']
            vehiculo.carroceria = request.POST['carroceria']
            vehiculo.anio = request.POST['anio']
            vehiculo.combustible = request.POST['combustible']
            vehiculo.transmision = request.POST['transmision']
            vehiculo.save()
            
            #Redireccionamos a la pagina de inicio
            return redirect('v_home')
            
        except Exception as e:
            print(f'Error al crear producto: {e}')
            #Modificar para que no se pierdan los datos <---
            return render(request, 'vendedor/v_home')

@login_required(login_url='acceso_usuario')
def v_eliminarProducto(request, id):
    if request.method == 'GET':
        try:
            producto = get_object_or_404(models.Producto, producto_id=id)
            producto.delete()
            return redirect('v_home')
        except models.Producto.DoesNotExist:
            return JsonResponse({'message': 'El vehículo no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error al eliminar el vehículo: {str(e)}'}, status=500)
    else:
        return JsonResponse('message', status=405)

#---- Accesorio ----
@login_required(login_url='acceso_usuario')
def v_paginaAccesorio(request, id):
    #Aqui nosotros obtenemos el producto que queremos mostrar
    if request.method == 'GET':
        
        user = request.user.id
        accesorio = models.Accesorio.objects.get(producto_id=id)

        llenar_datos ={
            'nombre': accesorio.nombre,
            'distribuidor': accesorio.distribuidor,
            'precio': accesorio.producto_id.precio,
            'descripcion': accesorio.producto_id.descripcion,
            'cantidad': accesorio.producto_id.cantidad
        }
        form = forms.registroAccesorio(initial=llenar_datos)
        context = {
            'accesorio': accesorio,
            'formulario': form,
            'titulo':'Detalles del Accesorio',
            'hiddenImagen':accesorio.producto_id.image,
            'hiddenId':accesorio.producto_id.producto_id,
            'hidenUser':user
        }
        return render(request, 'vendedor/paginaAccesorio.html', context)

def registroAccesorio(request):
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
                image = settings.MEDIA_URL + 'db-images/vehiculos/' + nameImg
            )
            #Guardamos el producto en la base de datos
            producto.save()
            print(producto)
            accesorio = models.Accesorio.objects.create(
                        producto_id=producto,
                        nombre = request.POST['nombre'],
                        distribuidor = request.POST['distribuidor']
            )
            print(accesorio)
            #guadamos el vehiculo en la base de datos
            accesorio.save()
            return redirect('v_home')
            
        except Exception as e:
            print(f'Error al crear producto: {e}')
            context = {
            'form': forms.registroAccesorio,
            'titulo': 'Accesorio',
        }
            return render(request, 'vendedor/registroAccesorio.html', context)
        
    
    elif request.method == 'GET':
        context = {
            'form': forms.registroAccesorio,
            'titulo': 'Accesorio'
        }
        return render(request,'vendedor/registroAccesorio.html', context)

def modificarAccesorio(request):
    #Aqui actualizaremos los datos del producto
    if request.method == 'POST':
        try:
            if 'imgProducto' in request.FILES:
                #nombre Archivo (Fecha y hora de guardado)
                nameImg = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png'
                #Creamos una ruta para guardar la imagen en el servidor
                imgPath = os.path.join(settings.MEDIA_ROOT, 'db-images/vehiculos/', nameImg)
                #verifica que el directorio existe (si no existe lo crea)
                os.makedirs(os.path.dirname(imgPath), exist_ok=True)
                #Creamos una instancia de la clase Image de la libreria PIL para guardar la imagen
                img = Image.open(request.FILES['imgProducto'])
                img.save(imgPath)
                #URL de la imagen para la base de datos
                imgURL = settings.MEDIA_URL + '/db-images/vehiculos/' + nameImg
            else:
                imgURL = request.POST['imgProductoOld']
            
            #Obtenemos los datos del producto y vehiculo de la base de datos
            producto_id = request.POST['idProducto']
            producto = models.Producto.objects.get(producto_id=producto_id)
            accesorio = models.Accesorio.objects.get(producto_id=producto)
            
            # Actualizamos los datos del producto
            producto.precio = request.POST['precio']
            producto.descripcion = request.POST['descripcion']
            producto.cantidad = request.POST['cantidad']
            producto.image = imgURL
            producto.save()
            
            # Actualizamos los datos del vehículo
            accesorio.nombre = request.POST['nombre']
            accesorio.distribuidor = request.POST['distribuidor']
            accesorio.producto_id = producto
            accesorio.save()
            
            #Redireccionamos a la pagina de inicio
            return redirect('v_home')
            
        except Exception as e:
            print(f'Error al crear producto: {e}')
            #Modificar para que no se pierdan los datos <---
            return render(request, 'vendedor/v_home')

#Funcion para deslogear al usuario
@login_required(login_url='acceso_usuario')
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

#---- Orden de Venta -----

@login_required(login_url='acceso_usuario')
def agregar_al_carrito(request):
    if request.method == 'POST':
        try:
            # Obtenemos los datos para generar la orden de compra
            cliente = request.user
            idProducto = request.POST.get('idProducto')
            cantidad = int(request.POST.get('cantidad'))
            
            # ---- Generar orden y detalle de compra -----

            # Obtenemos los datos del producto
            producto = get_object_or_404(models.Producto, producto_id=idProducto)
            print(producto)
            
            # Obtenemos la orden de compra del cliente, si existe
            orden, created = models.OrdenCompra.objects.get_or_create(cliente=cliente, completada=False)

            #Calculamos el subtotal del detalle
            subtotal = producto.precio * cantidad

            # Añadimos el producto a la orden de compra
            models.DetalleOrden.objects.create(
                orden=orden,
                producto=producto,
                cantidad=cantidad,
                subtotal=producto.precio * cantidad
            )
            
            # Redireccionamos a la vista del carrito o a donde sea necesario
            return redirect('home')  # Asegúrate de que 'home' sea el nombre correcto de tu vista
        except Exception as e:
            print(f"Error en agregar_al_carrito: {str(e)}")
            return HttpResponse("Hubo un error al procesar la solicitud.", status=500)

@login_required(login_url='acceso_usuario')
def facturar(request):
    try:
        # Obtenemos el nombre de usuario del usuario actual
        username = request.user.username
        
        # Obtener la orden de compra para el usuario actual que aún no está completada
        orden = models.OrdenCompra.objects.get(cliente__username=username, completada=False)
        
        # Obtener los detalles de la orden
        detalles = models.DetalleOrden.objects.filter(orden=orden)

        # Calcular el total de la factura
        total = sum(item.producto.precio * item.cantidad for item in detalles)

        # Generar la factura
        try:
            factura = models.Factura.objects.create(
                orden=orden,
                total=total
            )
            
            # Marcar la orden como completada
            orden.completada = True
            orden.save()
            
            return redirect('home')
        
        except Exception as e:
            # Imprimir el error para depuración
            print(f"Error al crear la factura: {e}")
            return HttpResponse('Bad Request 2')
    
    except models.OrdenCompra.DoesNotExist:
        return HttpResponse('No Order Found')
    
    except Exception as e:
        # Imprimir el error para depuración
        print(f"Error al procesar la facturación: {e}")
        return HttpResponse('Bad Request')

@login_required(login_url='acceso_usuario')
def eliminar_de_carrito(request):
    try:
        # Obtenemos los datos para eliminar el detalle de la orden
        idDetalle = request.POST.get('idDetalle')
        # Obtenemos los datos del detalle
        detalle = get_object_or_404(models.DetalleOrden, pk=idDetalle)
        # Eliminar el detalle de la orden
        detalle.delete()
        # Redireccionamos a la vista del carrito o a donde sea necesario
        return redirect('carrito')
    except Exception as e:
        print(f"Error en eliminar_de_carrito: {str(e)}")
        return HttpResponse("Hubo un error al procesar la solicitud.", status=500)
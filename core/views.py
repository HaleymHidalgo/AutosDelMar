from django.shortcuts import render, redirect
from . import models, forms

# Create your views here.
def home(request):
    if request.method == 'GET':
        #Aqui nosotros obtenemos todos los productos que estan en la base de datos
        vehiculos = models.Vehiculo.objects.all()
        context = {'vehiculos': vehiculos}
        #le vamos a pasarle el contexto a la plantilla
        return render(request, 'home.html', context)

def carrito(request):
    return render(request, 'carrito.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def paginaProducto(request, id):
    #Aqui nosotros obtenemos el producto que queremos mostrar
    vehiculo = models.Vehiculo.objects.get(producto_id=id)
    context = {
        'vehiculo': vehiculo,
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
    #Si se accede por metodo POST, guardamos el usuario en la base de datos
    if (request.method == 'POST'):
        form = forms.registroUsuario(request.POST)
        #Validamos el formulario
        if form.is_valid():
            if (request.POST['password'] == request.POST['password_confirm']):
                #Aqui creamos una instancia de la clase Usuario con los datos del formulario
                usuario = models.Usuario.create(
                    usuario_id=request.POST['usuario_id'],
                    nombre=request.POST['nombre'],
                    apellidop=request.POST['apellidop'],
                    apellidom=request.POST['apellidom'],
                    email=request.POST['email'],
                    nr_telefono=request.POST['nr_telefono'],
                    contraseña=request.POST['password']
                )
                #Guardamos el usuario en la base de datos y redireccionamos a la pagina de inicio
                usuario.save()
                #redirect recibe por parametro la url a la que queremos redireccionar (o el nombre)
                return redirect(home)
        
        #Si no es valido, mostramos el formulario con los errores
        else:
            return render(request, 'acceso/registro.html', {
                    'form': forms.registroUsuario,
                    'error': 'Datos incorrectos, intente de nuevo.'
                })
    
    return render(request, 'acceso/registro.html', {'form': forms.registroUsuario})





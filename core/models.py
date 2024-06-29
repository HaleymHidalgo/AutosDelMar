from django.db import models

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    precio=models.IntegerField()
    descripcion=models.CharField( max_length=250)
    cantidad= models.IntegerField()
    estado_producto = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/db-img/', default='media/db-img/default.jpg')
    
class Accesorios(models.Model):
    producto_id=models.ForeignKey(Producto,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=100)
    distribuidor=models.CharField(max_length=100)
    
class Vehiculo(models.Model):
    #No es un campo de texto, es un Objecto Producto
    producto_id=models.ForeignKey(Producto,on_delete=models.CASCADE)
    marca=models.CharField(max_length=100)
    modelo=models.CharField(max_length=100)
    carroceria=models.CharField(max_length=50)
    anio=models.IntegerField()
    combustible=models.CharField(max_length=50)
    transmision=models.CharField(max_length=50)
    
class Usuario(models.Model):
    usuario_id=models.CharField(max_length=10, primary_key=True)   
    nombre=models.CharField(max_length=50)
    apellidop=models.CharField(max_length=50)
    apellidom=models.CharField(max_length=50)
    email=models.CharField(max_length=150)
    nr_telefono=models.CharField(max_length=15)
    contraseña= models.CharField(max_length=50)
    tipo_usuario=models.CharField(max_length=50, default="cliente")
    estado_usuario=models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " " + self.apellidop + " " + self.apellidom
    
    @classmethod
    def create(cls, usuario_id, nombre, apellidop, apellidom, email, nr_telefono, contraseña):
        Usuario = cls(usuario_id=usuario_id,
                        nombre=nombre, 
                        apellidop=apellidop, 
                        apellidom=apellidom, 
                        email=email,
                        nr_telefono=nr_telefono,
                        contraseña=contraseña)
        return Usuario
        
class Venta(models.Model):
    venta_id=models.IntegerField(primary_key=True)
    fecha_venta=models.DateField()
    total_venta=models.IntegerField()
    cliente_run=models.ForeignKey( Usuario,on_delete=models.CASCADE)
    

class Venta_Producto(models.Model):
    venta_id=models.ForeignKey(Producto,on_delete=models.CASCADE)
    producto_id=models.ForeignKey(Venta,on_delete=models.CASCADE)
    cantidad_producto=models.IntegerField()
    subtotal_producto= models.IntegerField()

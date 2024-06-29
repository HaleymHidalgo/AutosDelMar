from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    precio=models.IntegerField()
    descripcion=models.CharField( max_length=250)
    cantidad= models.IntegerField()
    estado_producto = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media/db-img/%Y-%m-%d-%h-%m-%s', default='media/db-img/default.jpg')
    
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
        
class Venta(models.Model):
    venta_id=models.IntegerField(primary_key=True)
    fecha_venta=models.DateField()
    total_venta=models.IntegerField()
    cliente_run=models.ForeignKey( User,on_delete=models.CASCADE)
    

class Venta_Producto(models.Model):
    venta_id=models.ForeignKey(Producto,on_delete=models.CASCADE)
    producto_id=models.ForeignKey(Venta,on_delete=models.CASCADE)
    cantidad_producto=models.IntegerField()
    subtotal_producto= models.IntegerField()

from django.db import models

class Producto(models.Model):
    producto_id = models.IntegerField(primary_key=True)
    Precio=models.IntegerField()
    descripcion=models.CharField( max_length=250)
    cantidad= models.IntegerField()
    estado_producto = models.BooleanField()
    
    
class Accesorios(models.Model):
    producto_id=models.ForeignKey(Producto,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=100)
    distribuidor=models.CharField(max_length=100)
    
class Vehiculo(models.Model):
    producto_id=models.ForeignKey(Producto,on_delete=models.CASCADE)
    marca=models.CharField(max_length=100)
    modelo=models.CharField(max_length=100)



class Tipo_usuario(models.Model):
    id_tipo_usuario=models.IntegerField(primary_key=True)
    nombre_tipo_usuario=models.CharField(max_length=50)
    
class Usuario(models.Model):
    usuario_id=models.IntegerField(primary_key=True)   
    nombre=models.CharField(max_length=50)
    apellidop=models.CharField(max_length=50)
    apellidom=models.CharField(max_length=50)
    email=models.CharField(max_length=150)
    nr_telefono=models.CharField(max_length=15)
    contraseña= models.CharField(max_length=50)
    estado_usuario=models.BooleanField()
        
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

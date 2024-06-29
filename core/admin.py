from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Producto)
admin.site.register(models.Accesorios)
admin.site.register(models.Vehiculo)
admin.site.register(models.Venta)
admin.site.register(models.Venta_Producto)
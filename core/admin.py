from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Producto)
admin.site.register(models.Accesorio)
admin.site.register(models.Vehiculo)
admin.site.register(models.Contacto)
# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class registroUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'RUT (sin puntos)',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña'
        }

class accesoUsuario(forms.Form):
    usuario_id = forms.CharField(label="RUT (sin puntos)", max_length=10)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class registroVehiculo(forms.Form):
    marca = forms.CharField(label= "la marca del vehiculo",max_length=30)
    modelo = forms.CharField(label= "el modelo del vehiculo",max_length=30)
    carroceria = forms.CharField(label= "la carroceria del vehiculo",max_length=30)
    combustible = forms.CharField(label= "el combustible del vehiculo",max_length=30)
    anio = forms.IntegerField(label= "el año del vehiculo")
    transmision = forms.CharField(label= "la transmisión del vehiculo",max_length=30)
    precio = forms.IntegerField(label= "el precio del vehiculo")
    cantidad = forms.IntegerField(label="cantidad de vehiculo")
    descripcion = forms.CharField(label="descripcion", max_length=250)
    image = forms.ImageField()
    
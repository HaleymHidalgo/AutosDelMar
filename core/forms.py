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

class formularioContacto(forms.Form):
    nombre = forms.CharField(label="Ingrese su nombre", max_length=50)
    apellido = forms.CharField(label="ingrese su apellido", max_length=50)
    telefono = forms.CharField(label="Ingrese su Telefono", max_length=50)
    correo = forms.EmailField(label="Ingrese su correo", max_length=50)

class accesoUsuario(forms.Form):
    usuario_id = forms.CharField(label="RUT (sin puntos)", max_length=10)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
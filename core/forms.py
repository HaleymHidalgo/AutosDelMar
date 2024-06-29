from django import forms

class registroUsuario(forms.Form):
    usuario_id = forms.CharField(label="RUT (sin puntos)", max_length=10)
    nombre = forms.CharField(label="Nombre", max_length=50)
    apellidop = forms.CharField(label="Apellido Paterno", max_length=50)
    apellidom = forms.CharField(label="Apellido Materno", max_length=50)
    email = forms.EmailField(label="Email")
    nr_telefono = forms.IntegerField(label="N° Telefono")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
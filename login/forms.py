from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import usuarios

class LoginForm(AuthenticationForm):
    nombre_usuario = forms.CharField(
        label='Nombre de Usuario', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre de usuario'})
    )

    contrasena = forms.CharField(
        label='Contraseña', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
    )

    class Meta:
        model = usuarios
        fields = ['nombre_usuario', 'contrasena']
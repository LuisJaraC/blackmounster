from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Pelicula, Transaccion

class UsuarioUserCreationForm(UserCreationForm):
    #campo email para formulario, dandole un label
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name', 'password1', 'password2']

    #validacion de email, si ya existe en la base de datos
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya existe')
        return email
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = '__all__'

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
                }),
            'fecha_fin': forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
                }),
        }

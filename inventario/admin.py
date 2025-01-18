from django.contrib import admin
from .models import Pelicula, Transaccion
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .forms import UsuarioUserCreationForm
# Register your models here.
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'director', 'genero', 'precio_compra', 'precio_arriendo', 'stock']
    search_fields = ['titulo', 'director', 'genero']
    ordering = ['titulo']

class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pelicula', 'tipo', 'fecha_inicio', 'fecha_fin', 'estado']
    search_fields = ['usuario', 'pelicula', 'tipo', 'estado']
    ordering = ['usuario']

class UsuarioAdmin(UserAdmin):
    #añade el formulario de creacion de usuario
    add_form = UsuarioUserCreationForm

    #añade los campos que se mostraran en el formulario de creacion de usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']

admin.site.unregister(User)#sacamos el user registrado por defecto
admin.site.register(User, UsuarioAdmin)#registramos el user y nuestro modelo
admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Transaccion, TransaccionAdmin)

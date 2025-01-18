from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    genero = models.CharField(choices=(('Accion','Accion'),
                              ('Ciencia Ficcion','Ciencia Ficcion'),
                              ('Terror','Terror'),
                              ('Suspenso','Suspenso'),
                              ('Romantica','Romantica'),
                              ('Comedia','Comedia'),
                              ('Drama','Drama'),
                              ('Crimen','Crimen'),
                              ('Animacion','Animacion'),
                              ))
    descripcion = models.TextField(default='Sin descripcion')
    precio_compra = models.DecimalField(max_digits=7, decimal_places=2)
    precio_arriendo = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.titulo
    
class Transaccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.OneToOneField(Pelicula, on_delete=models.CASCADE)
    tipo = models.CharField(choices=(('Compra','Compra'),('Arriendo','Arriendo')))
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(choices=(('Pendiente','Pendiente'),('Completada','Completada')))

    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo}"
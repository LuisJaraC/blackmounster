from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from .models import User, Pelicula, Transaccion
from django.utils import timezone
# Create your tests here.

class TestTransacciones(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create(
            username="admin", password='pass')
        cls.pelicula = Pelicula.objects.create(
            titulo="Pelicula",
            director="director",
            genero="Drama",
            descripcion="Descripcion",
            precio_compra=1234.12,
            precio_arriendo=234.12,
            stock=10)
        cls.transaccion = Transaccion.objects.create(
            usuario = cls.usuario,
            pelicula = cls.pelicula,
            tipo = 'Arriendo',
            fecha_inicio = timezone.now(),
            fecha_fin=timezone.now(),
            estado = 'Completada'
        )

    def test_datos(self):
        usuario = User.objects.get(pk=1)
        pelicula = Pelicula.objects.get(pk=1)
        transaccion = Transaccion.objects.get(pk=1)

        self.assertEqual(usuario.username, "admin")
        self.assertEqual(pelicula.titulo, "Pelicula")
        self.assertEqual(pelicula.stock, 10)
        self.assertEqual(usuario.check_password('pass'))
        self.assertEqual(transaccion.estado, 'Completada')

    

    
    def test_url(self):
        response = self.client.get(reverse('transacciones'))
        self.assertEqual(response.status_code, 200)


    def test_transaccion(self):
        datos = {
            'usuario' : self.usuario.id,
            'pelicula' : self.pelicula.id,
            'tipo' : 'Arriendo',
            'fecha_inicio' : timezone.now(),
            'fecha_fin': timezone.now(),
            'estado' : 'Completada',
        }
        response = self.client.post(reverse('transacciones:nueva'), datos)

            
            


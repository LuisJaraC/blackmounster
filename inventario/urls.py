from django.urls import path
from .views import index, registroUsuario, loginView, logoutView, peliculasView, peliculasDetalle, peliculaNueva, peliculaEditar, peliculaEliminar, transacciones, nuevaTransaccion, detalleTransaccion

urlpatterns = [
    path('', index, name='index'),
    path('registro/', registroUsuario, name='registro'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('peliculas/', peliculasView, name='peliculas'),
    path('peliculas/<int:pk>', peliculasDetalle, name='detalle peliculas'),
    path('peliculas/nueva/', peliculaNueva, name='nueva pelicula'),
    path('peliculas/<int:pk>/editar/', peliculaEditar, name='editar pelicula'),
    path('peliculas/<int:pk>/eliminar/', peliculaEliminar, name='eliminar pelicula'),
    path('transacciones/', transacciones, name='transacciones'),
    path('transacciones/nueva/', nuevaTransaccion, name='nueva transaccion'),
    path('transacciones/<int:pk>', detalleTransaccion, name='detalle transaccion')

]
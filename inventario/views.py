from django.shortcuts import render, redirect,  get_object_or_404
from .forms import UsuarioUserCreationForm, LoginForm, PeliculaForm, TransaccionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Pelicula, Transaccion



# Create your views here.
def index(request):
    return render(request, 'index.html')

def registroUsuario(request):
    if request.method == 'POST':
        form = UsuarioUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente')
            return render(request, 'index.html')
    else:
        form = UsuarioUserCreationForm()
    return render(request, 'auth/registro.html', {'form': form})

def loginView(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Sesión iniciada exitosamente')
                return redirect('index')
            else:
                return render(request, 'auth/login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'auth/login.html', {'form': form})

def logoutView(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('index')

def peliculasView(request):
    peliculas = Pelicula.objects.all()
    context = {
        'peliculas': peliculas
    }
    return render(request, 'crud/peliculas.html', context)

def peliculasDetalle(request, pk):
    pelicula = Pelicula.objects.get(id=pk)
    context = {
        'pelicula': pelicula
    }
    return render(request, 'crud/pelicula_detalle.html', context)

def peliculaNueva(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pelicula registrada exitosamente')
            return redirect('peliculas')
    else:
        form = PeliculaForm()
    return render(request, 'crud/pelicula_nueva.html', {'form': form})

def peliculaEditar(request, pk):
    pelicula = Pelicula.objects.get(id=pk)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, instance=pelicula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pelicula editada exitosamente')
            return redirect('peliculas')
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'crud/pelicula_editar.html', {'form': form})

def peliculaEliminar(request, pk):
    pelicula = Pelicula.objects.get(id=pk)
    pelicula.delete()
    messages.success(request, 'Pelicula eliminada exitosamente')
    return redirect('peliculas')

def transacciones(request):
    if request.user.is_staff:
        transaccion = Transaccion.objects.all()
    else:
        transaccion = Transaccion.objects.filter(usuario=request.user)
    return render(request, 'crud/transacciones.html', {'transacciones': transaccion})

def nuevaTransaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            #verificacion para saber si el usuario es admin
            if request.user.is_staff:
                # si es usuario le asignamos el usuario del formulario
                if 'usuario' in form.cleaned_data:
                    transaccion.usuario = form.cleaned_data['usuario']
                else:
                    messages.error(request,'Debe seleccionar un usuario')
                    return redirect('transacciones')
            else:
                transaccion.usuario = request.user # le asigna la transaccion al usuario
            pelicula = transaccion.pelicula #obtener pelicula 
            #verificacion para ver si hay stock disponible
            if pelicula.stock <= 0:
                messages.error(request,'No hay stock disponible para la transaccion')
                return redirect('transacciones')
            transaccion.save()
            #actualizacion del stock
            pelicula.stock-=1
            pelicula.save()
            messages.success(request, 'Transacción registrada exitosamente')
            return redirect('transacciones')
    else:
        form = TransaccionForm()
        if not request.user.is_staff:
            form.fields['usuario'].required = False # para que el usuario no ingrese el campo usuario
    return render(request, 'crud/transaccion_nueva.html', {'form': form})


def detalleTransaccion(request, pk):
    #se obtiene la transaccion por medio del id y solo se hace si el usuario quien creo la transaccion es quien la busca
    transaccion = get_object_or_404(Transaccion, id=pk)
    #si el usuario es el dueño de la transaccion o es admin
    if transaccion.usuario == request.user or request.user.is_staff:
        return render(request, 'crud/transaccion_detalle.html', {'transaccion': transaccion})
    else:
        # Si el usuario no es el propietario ni un administrador, podemos redirigir o mostrar un error
        return render(request, 'crud/error.html', {'message': 'No tienes permiso para ver esta transacción.'})

def editarTransaccion(request, pk):
    #se obtiene la transaccion por medio del id y solo se hace si el usuario quien creo la transaccion es quien la busca
    transaccion = get_object_or_404(Transaccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        #se crea el form con los datos junto a la instancia de la transaccion
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            return redirect('transacciones')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'transacciones/editar.html', {'form': form})


def eliminarTransaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        transaccion.delete()
        return redirect('transacciones')
    return render(request, 'transacciones/eliminar.html', {'transaccion': transaccion})

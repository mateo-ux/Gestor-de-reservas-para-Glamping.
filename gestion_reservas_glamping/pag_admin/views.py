from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from pag_admin.forms import CrearGlampingForm
from .serializers import GlampingSerializer
from rest_framework import generics
import shutil
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReservaSerializer
from .models import Glamping, Reserva

# Verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser

# Vista protegida
@user_passes_test(is_superuser, login_url='/admin/login/')
def glamping_crear(request):
    if request.method == 'POST':
        form = CrearGlampingForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el nombre del glamping del formulario
            nombre_glamping = form.cleaned_data['nombre']
            # Definir la ruta donde se creará la carpeta
            folder_path = os.path.join('media', nombre_glamping)            
            # Verificar si ya existe una carpeta con el mismo nombre
            if os.path.exists(folder_path):
                form.add_error('nombre', f'Ya existe una carpeta con el nombre "{nombre_glamping}". Elige otro nombre.')
            else:
                # Guardar el formulario y crear la carpeta si no existe
                glamping = form.save(commit=False)
                os.makedirs(folder_path, exist_ok=True)  # Crear la carpeta
                glamping.save()  # Guardar la instancia en la base de datos                
                # Redirigir después de guardar
                return redirect('glampings_index')
    else:
        form = CrearGlampingForm()

    return render(request, 'admin/crearGlamping.html', {
        'form': form
    })
def glamping_eliminar(request, glamping_id):
    if request.method == 'POST':
        # Obtener el objeto Glamping
        glamping = get_object_or_404(Glamping, pk=glamping_id)        
        # Definir la ruta de la carpeta a eliminar (ajusta según la estructura de tu proyecto)
        ruta_carpeta = os.path.join('media', glamping.nombre)        
        # Verificar si la carpeta existe y eliminarla
        if os.path.exists(ruta_carpeta) and os.path.isdir(ruta_carpeta):
            shutil.rmtree(ruta_carpeta)  # Eliminar la carpeta y su contenido        
        # Eliminar el objeto Glamping de la base de datos
        glamping.delete()        
        # Redirigir al índice de glampings
        return redirect('glampings_index')    
    # Si el método no es POST, redirigir a la página principal
    return redirect('glampings_index')



def glamping_eliminar_carpeta(glamping):
    """
    Elimina la carpeta actual del glamping si existe.
    """
    ruta_carpeta = os.path.join(settings.MEDIA_ROOT, glamping.nombre)  # Usar settings.MEDIA_ROOT para asegurar la ruta correcta
    if os.path.exists(ruta_carpeta) and os.path.isdir(ruta_carpeta):
        shutil.rmtree(ruta_carpeta)  # Eliminar la carpeta y su contenido

def crear_nueva_carpeta(glamping):
    """
    Crea una nueva carpeta para el glamping si no existe.
    """
    nueva_carpeta = os.path.join(settings.MEDIA_ROOT, glamping.nombre)
    if not os.path.exists(nueva_carpeta):
        os.makedirs(nueva_carpeta)

def mover_imagenes_a_nueva_carpeta(glamping):
    """
    Mueve las nuevas imágenes a la nueva carpeta del glamping.
    """
    imagenes = [glamping.imagen1, glamping.imagen2, glamping.imagen3, glamping.imagen4, 
                glamping.imagen5, glamping.imagen6]
    
    # Definir la ruta de la nueva carpeta
    nueva_carpeta = os.path.join(settings.MEDIA_ROOT, glamping.nombre)
    
    # Mover las imágenes a la nueva carpeta
    for imagen in imagenes:
        if imagen:
            nueva_ruta = os.path.join(nueva_carpeta, os.path.basename(imagen.path))
            if os.path.exists(imagen.path):
                shutil.move(imagen.path, nueva_ruta)  # Mover imagen a la nueva carpeta

def glamping_actualizar(request, glamping_id):
    """
    Vista para actualizar un Glamping existente.
    """
    glamping = get_object_or_404(Glamping, pk=glamping_id)  # Obtener el objeto Glamping
    if request.method == 'POST':
        form = CrearGlampingForm(request.POST, request.FILES, instance=glamping)
        if form.is_valid():
            # Eliminar la carpeta anterior antes de la actualización
            glamping_eliminar_carpeta(glamping)
            
            # Guardar el glamping actualizado sin cometer inmediatamente
            glamping_actualizado = form.save(commit=False)

            # Crear la nueva carpeta para almacenar las imágenes (con el nombre actualizado)
            crear_nueva_carpeta(glamping_actualizado)
            
            # Guardar el glamping actualizado
            glamping_actualizado.save()

            # Mover las imágenes nuevas a la nueva carpeta
            mover_imagenes_a_nueva_carpeta(glamping_actualizado)
            
            return redirect('glampings_index')
    else:
        form = CrearGlampingForm(instance=glamping)
    
    return render(request, 'admin/actualizarGlamping.html', {
        'glamping': glamping,
        'form': form
    })


    
def glampings_index(request):
    glampings = Glamping.objects.all() # pylint: disable=E1101
    return render(request, 'admin/glampingIndex.html',{
        'glampings': glampings
    }) 


    


class GlampingList(generics.ListCreateAPIView):
    queryset = Glamping.objects.all() # pylint: disable=E1101
    serializer_class = GlampingSerializer
 
 ################################################################################################
 




@api_view(['POST'])
def crear_reserva(request):
    data = request.data
    glamping_id = data.get('glamping_id')
    fecha_inicio = data.get('checkInDate')
    fecha_fin = data.get('checkOutDate')

    # Verificar que todas las fechas están presentes
    if not all([glamping_id, fecha_inicio, fecha_fin]):
        return Response({'error': 'Datos incompletos'}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el glamping
    try:
        glamping = Glamping.objects.get(id=glamping_id) # pylint: disable=E1101
    except Glamping.DoesNotExist: # pylint: disable=E1101
        return Response({'error': 'Glamping no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Crear y guardar la reserva
    reserva = Reserva(
        glamping_id=glamping,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    try:
        reserva.save()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = ReservaSerializer(reserva)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from pag_admin.models import Glamping
from pag_admin.forms import CrearGlampingForm

import os
from .forms import CrearGlampingForm

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
    
def glamping_actualizar(request,glamping_id):
    if request.method == 'GET':
        glamping = Glamping.objects.get(pk = glamping_id) # pylint: disable=E1101
        form = CrearGlampingForm(instance = glamping)
        return render(request, 'admin/actualizarGlamping.html',{
            'glamping': glamping, 'form': form
        })
    else:
        glamping = Glamping.objects.get(pk = glamping_id) # pylint: disable=E1101
        form = CrearGlampingForm(request.POST, instance = glamping)
        form.save()
        return redirect('glampings_index')


    
def glampings_index(request):
    glampings = Glamping.objects.all() # pylint: disable=E1101
    return render(request, 'admin/glampingIndex.html',{
        'glampings': glampings
    }) 


    
def glamping_eliminar(request,glamping_id):
    if request.method == 'POST':
        glamping = Glamping.objects.get(pk = glamping_id) # pylint: disable=E1101
        glamping.delete()
        return redirect('glampings_index')
    else:
        return redirect('glampings_index')
    
    # views.py

from rest_framework import generics
from .serializers import GlampingSerializer

class GlampingList(generics.ListCreateAPIView):
    queryset = Glamping.objects.all() # pylint: disable=E1101
    serializer_class = GlampingSerializer


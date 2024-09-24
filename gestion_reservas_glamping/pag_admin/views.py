from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from .serializers import FechasOcupadasSerializer
from rest_framework.decorators import api_view
from pag_admin.forms import CrearGlampingForm
from rest_framework.response import Response
from .serializers import GlampingSerializer
from .serializers import ReservaSerializer
from .models import Glamping, Reserva
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from django.conf import settings
from datetime import timedelta
from datetime import datetime
import hashlib
import shutil
import json
import os

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
 

from django.db import IntegrityError, DatabaseError
from django.db.models import Q

@api_view(['POST'])
def crear_reserva(request):
    data = request.data
    glamping_id = data.get('glamping_id')
    fecha_inicio = data.get('checkInDate')
    fecha_fin = data.get('checkOutDate')

    # Verificar que todas las fechas están presentes
    if not all([glamping_id, fecha_inicio, fecha_fin]):
        return Response({'error': 'Datos incompletos'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar que la fecha de inicio es anterior a la fecha de fin
    if fecha_inicio >= fecha_fin:
        return Response({'error': 'La fecha de entrada debe ser anterior a la fecha de salida'}, status=status.HTTP_400_BAD_REQUEST)

    # Obtener el glamping
    try:
        glamping = Glamping.objects.get(id=glamping_id)  # pylint: disable=E1101
    except Glamping.DoesNotExist:  # pylint: disable=E1101
        return Response({'error': 'Glamping no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Verificar si las fechas nuevas solapan con alguna reserva existente para este glamping
    reservas_existentes = Reserva.objects.filter(  # pylint: disable=E1101
        glamping_id=glamping
    ).filter(
        Q(fecha_inicio__lte=fecha_fin) & Q(fecha_fin__gte=fecha_inicio)
    )

    if reservas_existentes.exists():
        return Response({'error': 'Ya existe una reserva en el rango de fechas seleccionado.'}, status=status.HTTP_400_BAD_REQUEST)

    # Crear y guardar la reserva
    reserva = Reserva(
        glamping_id=glamping,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    try:
        reserva.save()
    except IntegrityError as e:
        return Response({'error': 'Error de integridad: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError as e:
        return Response({'error': 'Error de base de datos: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = ReservaSerializer(reserva)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def fechas_ocupadas(request):
    glamping_id = request.GET.get('glamping_id')
    
    # Obtener las reservas asociadas a este glamping
    reservas = Reserva.objects.filter(glamping_id=glamping_id) # pylint: disable=E1101

    # Crear una lista de fechas ocupadas
    lista_fechas_ocupadas = []

    for reserva in reservas:
        fecha_inicial = reserva.fecha_inicio
        fecha_final = reserva.fecha_fin
        current_date = fecha_inicial

        while current_date <= fecha_final:
            lista_fechas_ocupadas.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)  # Mover al siguiente día

    # Serializar la lista de fechas ocupadas
    serializer = FechasOcupadasSerializer(data={'fechas_ocupadas': lista_fechas_ocupadas})
    
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def todas_fechas_ocupadas(request):
    glamping_id = request.GET.get('glamping_id')
    check_in = request.GET.get('checkIn')
    check_out = request.GET.get('checkOut')

    # Convertir fechas de string a objeto datetime
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        return Response({"error": "Fechas inválidas"}, status=400)

    # Filtrar por fechas y glamping_id (si está presente)
    if glamping_id:
        reservas = Reserva.objects.filter( # pylint: disable=E1101
            glamping_id=glamping_id,
            fecha_inicio__lte=check_out_date,
            fecha_fin__gte=check_in_date
        )
    else:
        reservas = Reserva.objects.filter( # pylint: disable=E1101
            fecha_inicio__lte=check_out_date,
            fecha_fin__gte=check_in_date
        )

    # Obtener todas las fechas ocupadas
    fechas_ocupadass = []
    for reserva in reservas:
        rango = [reserva.fecha_inicio + timedelta(days=x) for x in range((reserva.fecha_fin - reserva.fecha_inicio).days + 1)]
        fechas_ocupadass.extend(rango)

    # Convertir a string
    fechas_ocupadas_str = [fecha.strftime('%Y-%m-%d') for fecha in fechas_ocupadass]

    # Filtrar glampings disponibles
    glampings_disponibles = Glamping.objects.exclude( # pylint: disable=E1101
        reserva__fecha_inicio__lte=check_out_date,
        reserva__fecha_fin__gte=check_in_date
    ).values_list('id', flat=True)

    return Response({
        "fechas_ocupadass": fechas_ocupadas_str,
        "glampings_disponibles": list(glampings_disponibles)
    })

class GlampingDetail(generics.RetrieveAPIView):
    queryset = Glamping.objects.all() # pylint: disable=E1101
    serializer_class = GlampingSerializer
    

######################################################################
#payu

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            currency = data.get('currency', 'COP')
            description = data.get('description')
            reference_code = data.get('referenceCode')

            if not all([amount, description, reference_code]):
                return JsonResponse({'error': 'Faltan datos en la solicitud'}, status=400)

            signature_str = f"{settings.PAYU_API_KEY}~{settings.PAYU_MERCHANT_ID}~{reference_code}~{amount}~{currency}"
            signature = hashlib.md5(signature_str.encode('utf-8')).hexdigest()

            payment_data = {
                "merchantId": settings.PAYU_MERCHANT_ID,
                "accountId": settings.PAYU_ACCOUNT_ID,
                "description": description,
                "referenceCode": reference_code,
                "amount": amount,
                "currency": currency,
                "signature": signature,
                "test": 1 if settings.PAYU_TESTING else 0,
                "buyerEmail": "mateosalgado555@gmail.com",
                "responseUrl": "http://localhost:3000/pages/payment-response",
            }

            payu_url = "https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu/" if settings.PAYU_TESTING else "https://checkout.payulatam.com/ppp-web-gateway-payu/"

            return JsonResponse({
                'payu_url': payu_url,
                'payment_data': payment_data,
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido en la solicitud'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)



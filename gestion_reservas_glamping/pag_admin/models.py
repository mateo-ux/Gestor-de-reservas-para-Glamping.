from django.db import models
from django.core.files.storage import FileSystemStorage
import os
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()

fs = FileSystemStorage(location='media/')

@deconstructible
class GlampingImagePath:
    def __call__(self, instance, filename):
        nombre_folder = instance.nombre
        upload_path = f'{nombre_folder}'
        return os.path.join(upload_path, filename)

class Glamping(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=100)
    descripcion = models.TextField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    imagen1 = models.ImageField(upload_to=GlampingImagePath())
    imagen2 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen3 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen4 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen5 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen6 = models.ImageField(upload_to=GlampingImagePath(), blank=True)

    def clean(self):
        # Definir la ruta de la carpeta que se va a crear
        folder_path = os.path.join('media', self.nombre)
        
        # Verificar si la carpeta ya existe
        if os.path.exists(folder_path):
            raise ValidationError(f'Ya existe un glamping con el nombre "{self.nombre}". Elige otro nombre.')


    

class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    glamping_id = models.ForeignKey(Glamping, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
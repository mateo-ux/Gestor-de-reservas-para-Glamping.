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
    descripcion = models.TextField()
    precio = models.IntegerField()
    imagen1 = models.ImageField(upload_to=GlampingImagePath())
    imagen2 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen3 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen4 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen5 = models.ImageField(upload_to=GlampingImagePath(), blank=True)
    imagen6 = models.ImageField(upload_to=GlampingImagePath(), blank=True)

    def clean(self):
        # Solo realizar la verificación si es una creación (no actualización)
        if not self.pk:  # Si no hay primary key, es una creación
            folder_path = os.path.join('media', self.nombre)
            
            # Verificar si la carpeta ya existe
            if os.path.exists(folder_path):
                raise ValidationError(f'Ya existe un glamping con el nombre "{self.nombre}". Elige otro nombre.')


class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    glamping_id = models.ForeignKey(Glamping, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f'Reserva {self.id} - {self.glamping_id}'

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")


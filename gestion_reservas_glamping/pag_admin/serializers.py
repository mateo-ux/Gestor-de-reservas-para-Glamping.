from rest_framework import serializers
from .models import Glamping

class GlampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glamping
        fields = '__all__'  # O especifica los campos específicos
        
from .models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'glamping_id', 'fecha_inicio', 'fecha_fin']
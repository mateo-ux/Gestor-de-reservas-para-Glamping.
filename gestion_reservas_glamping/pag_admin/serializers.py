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
        

class FechasOcupadasSerializer(serializers.Serializer):
    """
    Serializador para las fechas ocupadas de un glamping.
    """
    fechas_ocupadas = serializers.ListField(child=serializers.DateField(format='%Y-%m-%d'))

    def create(self, validated_data):
        # No se implementa lógica de creación
        pass

    def update(self, instance, validated_data):
        # No se implementa lógica de actualización
        pass



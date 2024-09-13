from rest_framework import serializers
from .models import Glamping

class GlampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Glamping
        fields = '__all__'  # O especifica los campos específicos
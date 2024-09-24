from django import forms
from .models import Glamping

class CrearGlampingForm(forms.ModelForm):
    class Meta:
        model = Glamping
        fields = ['nombre', 'descripcion', 'precio', 'imagen1', 'imagen2', 'imagen3', 'imagen4', 'imagen5', 'imagen6']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input input-bordered flex items-center gap-2'}),
            'descripcion': forms.TextInput(attrs={'class': 'input input-bordered flex items-center gap-2'}),
            'precio': forms.TextInput(attrs={'class': 'input input-bordered flex items-center gap-2'}),
        }

    def __init__(self, *args, **kwargs):
        # Recibimos 'is_update' para saber si es actualización
        is_update = kwargs.pop('is_update', False)
        super(CrearGlampingForm, self).__init__(*args, **kwargs)

        if is_update:
            # Hacemos el campo 'nombre' de solo lectura si es actualización
            self.fields['nombre'].widget.attrs['readonly'] = True

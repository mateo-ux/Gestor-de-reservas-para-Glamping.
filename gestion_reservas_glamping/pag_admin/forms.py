from django import forms
from .models import Glamping

class CrearGlampingForm(forms.ModelForm):
    class Meta:
        model = Glamping
        fields = ['nombre','descripcion','imagen1','imagen2','imagen3','imagen4','imagen5','imagen6']
        widgets = {
            'nombre': forms.TextInput(attrs = {'class': 'input input-bordered flex items-center gap-2'}),
            'descripcion': forms.TextInput(attrs = {'class':'input input-bordered flex items-center gap-2'}),
            
        }
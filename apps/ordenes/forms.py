# forms.py
from .models import Equipos
from django import forms

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ['numero_serie', 'observaciones']
from django import forms
from .models import Remitos

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remitos
        fields = ['numero_remito', 'numero_viaje', 'detalle_transporte', 'deposito_id', 'fecha_ingreso', 'usuario_id', 'aprobado']
        
                
# class ProductoForm(forms.ModelForm):
#     class Meta:
#         model = Producto
#         fields = ['marca', 'modelo', 'deposito']

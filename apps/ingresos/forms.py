from django import forms
from .models import Remitos

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remitos
        fields = ['numero_remito', 'numero_viaje', 'detalle_transporte', 'deposito_id', 'fecha_ingreso', 'usuario_id', 'aprobado']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'},
                                             format='%Y-%m-%d'
                                             )
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reapply format manually if initial value exists
        if self.initial.get('fecha_ingreso') and isinstance(self.initial['fecha_ingreso'], str) is False:
            self.initial['fecha_ingreso'] = self.initial['fecha_ingreso'].strftime('%Y-%m-%d')
                
# class ProductoForm(forms.ModelForm):
#     class Meta:
#         model = Producto
#         fields = ['marca', 'modelo', 'deposito']

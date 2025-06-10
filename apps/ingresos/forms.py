from django import forms
from .models import Remitos, Productos, RemitoProducto
from django.forms.models import inlineformset_factory

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remitos
        fields = ['numero_remito', 'numero_viaje', 'detalle_transporte', 'deposito_id', 'fecha_ingreso', 'usuario_id', 'aprobado']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'},
                                             format='%Y-%m-%d'
                                             )
        }
RemitoProductoFormSet = inlineformset_factory(
    Remitos,
    RemitoProducto,
    fields=['producto_id', 'cantidad'],
    extra=1,
    can_delete=True
)
        
def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reapply format manually if initial value exists
        if self.initial.get('fecha_ingreso') and isinstance(self.initial['fecha_ingreso'], str) is False:
            self.initial['fecha_ingreso'] = self.initial['fecha_ingreso'].strftime('%Y-%m-%d')

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__' 

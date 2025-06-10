# apps/despachos/admin.py

from django.contrib import admin
from .models import Pallet, DetallePallet # Asegúrate de que Pallet y DetallePallet estén importados

class DetallePalletInline(admin.TabularInline):
    """
    Clase Inline para mostrar los DetallePallet directamente
    en la página de edición de Pallet en el administrador de Django.
    
    """
    model = DetallePallet
    extra = 1

@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    """
    Configuración para la gestión del modelo Pallet en Django Admin.
    Hemos actualizado 'list_display' para reflejar los nuevos nombres de campos
    en el modelo Pallet.
    """
    # ¡NOMBRES DE CAMPOS ACTUALIZADOS EN list_display!
    list_display = ('id', 'orden', 'fecha_creacion', 'fecha_despacho', 'usuario_id', 'remito_salida', 'destino_id', 'nro_pallet', 'nro_viaje')
    inlines = [DetallePalletInline]

@admin.register(DetallePallet)
class DetallePalletAdmin(admin.ModelAdmin):
    """
    Configuración para la gestión del modelo DetallePallet en Django Admin.
    """
    list_display = ('id', 'pallet', 'descripcion')
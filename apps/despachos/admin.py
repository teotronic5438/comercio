# apps/despachos/admin.py

from django.contrib import admin
from .models import Pallet, DetallePallet # Asegúrate de que los modelos estén importados

# Inline para mostrar los detalles del pallet directamente en la edición del Pallet
class DetallePalletInline(admin.TabularInline):
    model = DetallePallet
    extra = 1 # Cuántos formularios vacíos mostrar por defecto
    # Los campos que quieres mostrar y/o permitir editar en el inline
    fields = ['orden_id', 'modelo', 'serial', 'cantidad']
    # Los campos de solo lectura si no quieres que se modifiquen desde el inline
    readonly_fields = ['modelo', 'serial'] # Por ejemplo, si estos se rellenan automáticamente


@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de Pallets en el admin
    list_display = (
        'id', # 'id' siempre es bueno mostrarlo
        'destino', # Antes era 'orden', ahora es 'destino' (el campo de ForeignKey directo)
        'nro_pallet',
        'fecha_creacion',
        'nro_viaje',
        'fecha_despacho',
        'usuario_id',
        'remito_salida',
    )
    # Campos por los que puedes buscar
    search_fields = (
        'nro_pallet',
        'nro_viaje',
        'destino__nombre_destino', # Para buscar por el nombre del destino
        'detalles__orden_id__equipo_id__numero_serie', # Para buscar por número de serie de las órdenes en el pallet
    )
    # Filtros laterales
    list_filter = (
        'destino',
        'fecha_creacion',
        'fecha_despacho',
        'usuario_id',
    )
    # Los inlines para mostrar DetallePallet dentro de Pallet
    inlines = [DetallePalletInline]
    # Campos que no se pueden editar después de la creación si es necesario
    readonly_fields = ['fecha_creacion']


@admin.register(DetallePallet)
class DetallePalletAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de DetallePallets en el admin
    list_display = (
        'id',
        'pallet', # El pallet al que pertenece
        'orden_id', # La orden asociada
        'modelo',
        'serial',
        'cantidad',
    )
    # Campos por los que puedes buscar
    search_fields = (
        'pallet__nro_pallet',
        'orden_id__id',
        'orden_id__equipo_id__numero_serie',
        'modelo',
        'serial',
    )
    # Filtros laterales
    list_filter = (
        'pallet__destino', # Puedes filtrar por el destino del pallet padre
        'cantidad',
    )
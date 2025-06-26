# apps/despachos/admin.py

from django.contrib import admin
from .models import Pallet, DetallePallet
from django.utils.html import format_html # Necesario para enlaces si los usamos
from django.urls import reverse # Necesario para enlaces si los usamos

# Inline para mostrar los detalles del pallet directamente en la edición del Pallet
class DetallePalletInline(admin.TabularInline):
    model = DetallePallet
    extra = 1 # Cuántos formularios vacíos mostrar por defecto
    
    # Mostrar la orden y sus datos relevantes
    # Usamos callable methods para acceder a los datos a través de la relación orden_id
    fields = ['orden_id', 'get_orden_numero_serie', 'get_orden_modelo', 'get_orden_marca']
    readonly_fields = ['get_orden_numero_serie', 'get_orden_modelo', 'get_orden_marca']

    def get_orden_numero_serie(self, obj):
        # Accede al número de serie de la orden asociada
        return obj.orden_id.equipo_id.numero_serie if obj.orden_id and obj.orden_id.equipo_id else 'N/A'
    get_orden_numero_serie.short_description = 'Nro. Serie Equipo' # Nombre de la columna en el admin

    def get_orden_modelo(self, obj):
        # Accede al modelo del producto del equipo de la orden asociada
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            # Asumiendo que 'modelo_id' es el ForeignKey al modelo de Producto
            # y que el modelo de Producto tiene un campo 'nombre_modelo' (o similar)
            return obj.orden_id.equipo_id.producto_id.modelo_id.nombre_modelo if obj.orden_id.equipo_id.producto_id.modelo_id else 'N/A'
        return 'N/A'
    get_orden_modelo.short_description = 'Modelo Equipo'

    def get_orden_marca(self, obj):
        # Accede a la marca del producto del equipo de la orden asociada
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            # Asumiendo que 'marca_id' es el ForeignKey a la marca de Producto
            # y que el modelo de Marca tiene un campo 'nombre_marca' (o similar)
            return obj.orden_id.equipo_id.producto_id.marca_id.nombre_marca if obj.orden_id.equipo_id.producto_id.marca_id else 'N/A'
        return 'N/A'
    get_orden_marca.short_description = 'Marca Equipo'


@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    # Ajustar list_display para los nuevos campos de usuario y estado
    list_display = (
        'id',
        'nro_pallet', # Se mantiene nro_pallet
        'destino',
        'estado_pallet', # Añadido el estado del pallet
        'fecha_creacion',
        'fecha_despacho',
        'usuario', # El usuario creador (de ModeloBaseConUsuario)
        'usuario_despacho', # El usuario que despacha el pallet
        'remito_salida',
        'get_cantidad_ordenes', # Método para mostrar la cantidad de órdenes en el pallet
    )
    # Campos por los que puedes buscar
    search_fields = (
        'nro_pallet',
        'nro_viaje',
        'destino__nombre_destino',
        'estado_pallet__nombre_estado', # Buscar por nombre de estado del pallet
        'usuario__username', # Buscar por el username del creador
        'usuario_despacho__username', # Buscar por el username del despachador
        'detalles__orden_id__equipo_id__numero_serie', # Buscar por número de serie de las órdenes
    )
    # Filtros laterales
    list_filter = (
        'destino',
        'estado_pallet', # Filtrar por estado del pallet
        'fecha_creacion',
        'fecha_despacho',
        'usuario', # Filtrar por el usuario creador
        'usuario_despacho', # Filtrar por el usuario que despachó
    )
    inlines = [DetallePalletInline]
    readonly_fields = ['fecha_creacion']

    # Método para mostrar la cantidad de órdenes en el list_display
    def get_cantidad_ordenes(self, obj):
        return obj.detalles.count()
    get_cantidad_ordenes.short_description = 'Órdenes' # Nombre de la columna


@admin.register(DetallePallet)
class DetallePalletAdmin(admin.ModelAdmin):
    # Ajustar list_display para acceder a los campos de la orden a través de la relación
    list_display = (
        'id',
        'pallet',
        'orden_id',
        'get_orden_numero_serie', # Usar método para el número de serie
        'get_orden_modelo', # Usar método para el modelo
        'get_orden_marca', # Usar método para la marca
        # 'cantidad', # Si ya no usas cantidad, puedes quitarlo
    )
    # Campos por los que puedes buscar
    search_fields = (
        'pallet__nro_pallet',
        'orden_id__id',
        'orden_id__equipo_id__numero_serie', # Buscar por el numero de serie de la orden
        'orden_id__equipo_id__producto_id__modelo_id__nombre_modelo', # Buscar por el modelo del producto
        'orden_id__equipo_id__producto_id__marca_id__nombre_marca', # Buscar por la marca del producto
    )
    # Filtros laterales
    list_filter = (
        'pallet__destino',
        'pallet__estado_pallet', # Filtrar por el estado del pallet al que pertenece
        # 'cantidad', # Si lo quieres como filtro, debe ser un campo en DetallePallet.
                     # Si 'cantidad' es siempre 1, no es útil como filtro.
                     # Si lo quitas de models.py, quítalo de aquí también.
    )

    # Estos métodos son necesarios aquí también para list_display
    def get_orden_numero_serie(self, obj):
        return obj.orden_id.equipo_id.numero_serie if obj.orden_id and obj.orden_id.equipo_id else 'N/A'
    get_orden_numero_serie.short_description = 'Nro. Serie Equipo'

    def get_orden_modelo(self, obj):
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            return obj.orden_id.equipo_id.producto_id.modelo_id.nombre_modelo if obj.orden_id.equipo_id.producto_id.modelo_id else 'N/A'
        return 'N/A'
    get_orden_modelo.short_description = 'Modelo Equipo'

    def get_orden_marca(self, obj):
        if obj.orden_id and obj.orden_id.equipo_id and obj.orden_id.equipo_id.producto_id:
            return obj.orden_id.equipo_id.producto_id.marca_id.nombre_marca if obj.orden_id.equipo_id.producto_id.marca_id else 'N/A'
        return 'N/A'
    get_orden_marca.short_description = 'Marca Equipo'
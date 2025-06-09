from django.contrib import admin
from .models import Estados, Destinos, Equipos, Ordenes, HistorialOrdenes

@admin.register(Estados)
class EstadosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_estado']
    search_fields = ['nombre_estado']


@admin.register(Destinos)
class DestinosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_destino']
    search_fields = ['nombre_destino']


@admin.register(Equipos)
class EquiposAdmin(admin.ModelAdmin):
    list_display = ['id', 'numero_serie', 'producto_id', 'fecha_alta']
    search_fields = ['numero_serie', 'producto_id']

'''
@admin.register(Ordenes)
class OrdenesAdmin(admin.ModelAdmin):
    list_display = ['id', 'remito_id', 'get_equipo', 'get_estado', 'orden_activa', 'fecha_creacion']
    list_filter = ['orden_activa']
    search_fields = ['id', 'equipo__numero_serie', 'estado__nombre_estado']

    @admin.display(description='Equipo')
    def get_equipo(self, obj):
        return obj.equipo.numero_serie

    @admin.display(description='Estado')
    def get_estado(self, obj):
        return obj.estado.nombre_estado
'''

from django import forms

class OrdenesAdminForm(forms.ModelForm):
    class Meta:
        model = Ordenes
        fields = ['remito_id', 'equipo_id']

class OrdenesAdmin(admin.ModelAdmin):
    form = OrdenesAdminForm
    readonly_fields = ('fecha_creacion', 'fecha_revision')
    list_display = ('id', 'equipo_id', 'estado_id', 'remito_id', 'orden_activa')

admin.site.register(Ordenes, OrdenesAdmin)

@admin.register(HistorialOrdenes)
class HistorialOrdenesAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_orden_id', 'descripcion', 'fecha_modificacion']
    search_fields = ['descripcion']

    @admin.display(description='Orden ID')
    def get_orden_id(self, obj):
        return obj.ordenes.id

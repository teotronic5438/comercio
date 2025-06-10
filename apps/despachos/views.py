# apps/despachos/views.py

from django.shortcuts import render
from django.utils.timezone import now
from apps.ordenes.models import Ordenes, Estados, Destinos


def ordenes_revisadas(request):
    """
    Vista para listar todas las órdenes que tienen el estado "revisado",
    preparando los datos en un formato de lista de diccionarios,
    similar a la estructura de ordenes_pendientes.
    """
    # Obtenemos la instancia del estado 'revisado'.
    estado_revisado = Estados.objects.get(nombre_estado__iexact="revisado")

    # Optimizamos la consulta cargando relaciones necesarias
    # ¡CORRECCIÓN CLAVE AQUÍ: Usamos estado_id para el filtro!
    ordenes_queryset = Ordenes.objects.filter(estado_id=estado_revisado).select_related(
        'destino',
        'equipo_id__producto_id',
        'estado_id'
    )

    # Creamos una lista para almacenar los diccionarios de datos de las órdenes revisadas.
    datos_ordenes_revisadas = []
    for orden in ordenes_queryset:
        # Capturamos el modelo del producto, manejando casos donde puede ser nulo
        producto_modelo = orden.equipo_id.producto_id.modelo if orden.equipo_id and orden.equipo_id.producto_id else 'N/A'

        # Capturamos el nombre del destino, manejando casos donde puede ser nulo
        nombre_destino = orden.destino.nombre_destino if orden.destino else 'Sin asignar'

        
        datos_ordenes_revisadas.append({
            'id': orden.id,
            'equipo_id': orden.equipo_id, # El objeto Equipo para que su __str__ sea llamado en el template
            'modelo': producto_modelo,
            'fecha_creacion': orden.fecha_creacion,
            'estado': orden.estado_id.nombre_estado, # Accedemos al nombre del estado
            'destino': nombre_destino,
            'falla_detectada': orden.falla_detectada,
            'reparacion': orden.reparacion,
            'fecha_revision': orden.fecha_revision,
        })

    # Pasamos la lista de diccionarios al template.
    return render(request, 'despachos/revisados.html', {'ordenes': datos_ordenes_revisadas})

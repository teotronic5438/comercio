from django.shortcuts import render, get_object_or_404, redirect
from .models import Ordenes, Estados, Destinos
from django.utils.timezone import now
# from datetime import timedelta
# from ingresos.models import Remitos  # si lo necesitás

# Create your views here.
def ordenes_pendientes(request):
    ordenes = Ordenes.objects.select_related(
        'equipo_id__producto_id', 'estado_id'
    ).filter(
        estado_id__nombre_estado='Pendiente'
    )

    datos_ordenes = []
    for orden in ordenes:
        producto_modelo = orden.equipo_id.producto_id.modelo
        fecha_creacion = orden.fecha_creacion
        tiempo_transcurrido = now() - fecha_creacion
        datos_ordenes.append({
            'id': orden.id,
            'modelo': producto_modelo,
            'fecha_creacion': fecha_creacion,
            'tiempo_transcurrido': tiempo_transcurrido,
            'estado': orden.estado_id.nombre_estado,
        })

    return render(request, 'ordenes/ordenes_pendientes.html', {
        'ordenes': datos_ordenes
    })


# def revisar_orden(request, orden_id):
#     orden = get_object_or_404(Ordenes, id=orden_id)

#     estados = Estados.objects.all()
#     destinos = Destinos.objects.all()

#     return render(request, 'ordenes/revisar_orden.html', {
#         'orden': orden,
#         'estados': estados,
#         'destinos': destinos,
#     })

def revisar_orden(request, orden_id):
    orden = get_object_or_404(Ordenes, id=orden_id)

    if request.method == 'POST':
        orden.falla_detectada = request.POST.get('falla_detectada')
        orden.reparacion = request.POST.get('reparacion')
        
        # Se actualiza el destino si se seleccionó uno
        destino_id = request.POST.get('destino')
        if destino_id:
            orden.destino_id = destino_id

        # Actualizar estado a "Revisado"
        estado_revisado = Estados.objects.get_or_create(nombre_estado='Revisado')[0]
        orden.estado_id = estado_revisado

        # Guardar fecha de revisión como ahora
        orden.fecha_revision = now()

        # Guardar cambios
        orden.save()

        # Redirigir a la lista de órdenes pendientes (o a otra vista de confirmación)
        return redirect('ordenes_pendientes')

    # GET: mostrar datos actuales
    estados = Estados.objects.all()
    destinos = Destinos.objects.all()

    return render(request, 'ordenes/revisar_orden.html', {
        'orden': orden,
        'estados': estados,
        'destinos': destinos,
    })
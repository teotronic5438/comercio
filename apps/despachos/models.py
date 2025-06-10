# apps/despachos/models.py

from django.db import models
# Importamos Ordenes desde apps.ordenes.models (esto sí está allí)
from apps.ordenes.models import Ordenes, Destinos, Estados
# ¡IMPORTACIONES CORREGIDAS!
# Importamos Remitos desde apps.ingresos.models
from apps.ingresos.models import Remitos
# Importamos Usuarios desde apps.usuarios.models
from apps.usuarios.models import Usuarios



class Pallet(models.Model):
    """
    Modelo para representar un Pallet en el sistema de despachos.
    Un pallet agrupa órdenes para su posterior despacho.
    """

    #Se cambia 'ordenes.destino' por Destinos. 
    destino_id = models.ForeignKey(Destinos, on_delete= models.CASCADE)
    nro_pallet = models.CharField(max_length=50, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nro_viaje = models.CharField(max_length=50, null=True, blank=True)
    fecha_despacho = models.DateTimeField(null=True, blank=True)
    orden = models.ForeignKey(Ordenes, on_delete=models.CASCADE)
    usuario_id = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    remito_salida = models.ForeignKey(Remitos, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"Pallet {self.id} - Orden {self.orden.id}"

class DetallePallet(models.Model):
    """
    Modelo para almacenar los detalles o descripciones de lo que contiene un Pallet.
    """
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE, related_name='detalles')
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f"Detalle Pallet {self.pallet.id}: {self.descripcion}"

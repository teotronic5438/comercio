# apps/despachos/models.py

from django.db import models
from apps.ordenes.models import Ordenes, Destinos, Estados
from apps.ingresos.models import Remitos # Asegúrate de que esta importación sea correcta si usas Remitos
from apps.usuarios.models import Usuarios # Asegúrate de que esta importación sea correcta si usas Usuarios

class Pallet(models.Model):
    """
    Modelo para representar un Pallet en el sistema de despachos.
    Un pallet agrupa órdenes para su posterior despacho.
    """
    destino = models.ForeignKey(Destinos, on_delete=models.PROTECT, related_name='pallets_despacho')
    nro_pallet = models.CharField(max_length=50, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nro_viaje = models.CharField(max_length=50, null=True, blank=True)
    fecha_despacho = models.DateTimeField(null=True, blank=True)
    usuario_id = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    remito_salida = models.ForeignKey(Remitos, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- NUEVO CAMPO DE ESTADO PARA EL PALLET ---
    estado_pallet = models.ForeignKey(Estados, on_delete=models.PROTECT, related_name='pallets_por_estado', null=True, blank=True)
    # --- FIN NUEVO CAMPO ---

    class Meta:
        verbose_name = "Pallet de Despacho"
        verbose_name_plural = "Pallets de Despacho"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Pallet {self.nro_pallet if self.nro_pallet else self.id} - Destino: {self.destino.nombre_destino if self.destino else 'N/A'}"

class DetallePallet(models.Model):
    """
    Modelo para los detalles de un Pallet, conectando Pallets con Órdenes.
    """
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE, related_name='detalles')
    orden_id = models.OneToOneField(Ordenes, on_delete=models.CASCADE, related_name='detalle_pallet')
    modelo = models.CharField(max_length=100, null=True, blank=True)
    serial = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1) # Generalmente 1 por orden, pero puede variar.

    class Meta:
        verbose_name = "Detalle de Pallet"
        verbose_name_plural = "Detalles de Pallet"
        unique_together = ('pallet', 'orden_id') # Una orden solo puede estar una vez en un pallet

    def __str__(self):
        return f"Detalle de Pallet {self.pallet.nro_pallet} - Orden {self.orden_id.id}"
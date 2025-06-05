from django.db import models

class Estados(models.Model):
    nombre_estado = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre_estado


class Destinos(models.Model):
    nombre_destino = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre_destino


class Equipos(models.Model):
    producto_id = models.IntegerField()
    numero_serie = models.CharField(max_length=20, unique=True)
    fecha_alta = models.DateTimeField()
    observaciones = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.numero_serie}"

class HistorialOrdenes(models.Model):
    descripcion = models.CharField(max_length=100)
    fecha_modificacion = models.DateTimeField()

    def __str__(self):
        return f"Historial de Orden {self.descripcion} - Fecha {self.fecha_modificacion}"

class Ordenes(models.Model):
    remito_id = models.ForeignKey('ingresos.Remitos', on_delete=models.CASCADE)
    equipo_id = models.ForeignKey(Equipos, on_delete=models.CASCADE)
    estado_id = models.ForeignKey(Estados, on_delete=models.CASCADE)
    falla_detectada = models.CharField(max_length=50)
    reparacion = models.CharField(max_length=50)
    fecha_revision = models.DateTimeField()
    usuario_id = models.ForeignKey('usuarios.Usuarios', on_delete=models.CASCADE)
    orden_activa = models.BooleanField()
    fecha_creacion = models.DateTimeField()
    modificacion_id = models.ForeignKey(HistorialOrdenes, on_delete=models.CASCADE, null=True, blank=True)
    destino = models.ForeignKey(Destinos, on_delete=models.CASCADE)

    def __str__(self):
        return f"Orden {self.id} - Modelo {self.equipo_id.numero_serie} - Estado {self.estado_id.nombre_estado}"




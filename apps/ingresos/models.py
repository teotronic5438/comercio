# Create your models here.
from django.db import models


class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.marca} - {self.modelo}"

class Remitos(models.Model):
    id = models.AutoField(primary_key=True)
    numero_remito = models.CharField(max_length=20)
    numero_viaje = models.IntegerField()
    detalle_transporte = models.CharField(max_length=30)
    deposito_id = models.ForeignKey('stock.Depositos', on_delete=models.PROTECT)
    fecha_ingreso = models.DateField()
    usuario_id = models.ForeignKey('usuarios.Usuarios', on_delete=models.PROTECT)
    aprobado = models.BooleanField()
    productos = models.ManyToManyField('Productos', through='RemitoProducto')
    
    def __str__(self):
        return f"{self.numero_remito}"


class RemitoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    remito_id = models.ForeignKey('Remitos', on_delete=models.CASCADE)
    producto_id = models.ForeignKey('Productos', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    actualizado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.producto_id} {self.cantidad} {self.remito_id}"
    
   



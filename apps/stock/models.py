from django.db import models
from apps.ingresos.models import Productos

# Create your models here.
class Depositos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class StockProductos(models.Model):
    id = models.AutoField(primary_key=True)
    producto_id = models.ForeignKey(Productos, on_delete=models.CASCADE)
    deposito_id = models.ForeignKey(Depositos, on_delete=models.CASCADE)
    cantidad_total = models.IntegerField()

    def __str__(self):
        return f"{self.producto} en {self.deposito}: {self.cantidad_total}"
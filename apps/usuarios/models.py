from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.nombre_usuario})"
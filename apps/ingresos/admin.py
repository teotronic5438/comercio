from django.contrib import admin

# Register your models here.

from .models import Productos, Remitos, RemitoProducto

admin.site.register(Productos)
admin.site.register(Remitos)
admin.site.register(RemitoProducto)



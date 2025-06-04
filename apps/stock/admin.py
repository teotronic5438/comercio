from django.contrib import admin

# Register your models here.
# traigo la tabla que quiero registrar
from .models import StockProductos, Depositos

# registro la tabla para que me aparezca en el panel
admin.site.register(StockProductos)
admin.site.register(Depositos)

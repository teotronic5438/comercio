from django.contrib import admin

# Register your models here.
# traigo la tabla que quiero registrar
from .models import StockProductos

# registro la tabla para que me aparezca en el panel
admin.site.register(StockProductos)

from django.contrib import admin

# Register your models here.
# traigo la tabla que quiero registrar
from .models import Stock

# registro la tabla para que me aparezca en el panel
admin.site.register(Stock)

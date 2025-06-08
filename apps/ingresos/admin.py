from django.contrib import admin

# Register your models here.

from .models import Productos, Remitos, RemitoProducto

# admin.site.register(Productos)
@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo')
    search_fields = ('marca', 'descmodelo')
    list_filter = ('marca',)

admin.site.register(Remitos)
admin.site.register(RemitoProducto)



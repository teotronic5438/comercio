# apps/usuarios/urls.py
# from django.urls import path
# from .views import test_view

# urlpatterns = [
    # path('test/', test_view),
# ]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import listar_remitos, crear_remito, editar_remito, eliminar_remito, aprobar_remito, listar_remitos_hitorial

#apis
from .views import remito_list, remito_create

urlpatterns = [
    path('ingresos/', listar_remitos, name='ingresos'),
    path('ingresos/history', listar_remitos_hitorial, name='ingresos_historial'),
    path('nuevo/', crear_remito, name='crear_remito'),
    path('editar/<int:pk>/', editar_remito, name='editar_remito'),
    path('eliminar/<int:pk>/', eliminar_remito, name='eliminar_remito'),
    path('aprobar/<int:pk>/', aprobar_remito, name='aprobar_remito'),
    path('remitos/', remito_list, name='remitos-list'),
    path('remitos/crear/', remito_create, name='remito-create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
# apps/usuarios/urls.py
# from django.urls import path
# from .views import test_view

# urlpatterns = [
    # path('test/', test_view),
# ]


from django.urls import path
from .views import listar_remitos, crear_remito, editar_remito, eliminar_remito, aprobar_remito

urlpatterns = [
    path('ingresos/', listar_remitos, name='ingresos'),
    path('nuevo/', crear_remito, name='crear_remito'),
    path('editar/<int:pk>/', editar_remito, name='editar_remito'),
    path('eliminar/<int:pk>/', eliminar_remito, name='eliminar_remito'),
    path('aprobar/<int:pk>/', aprobar_remito, name='aprobar_remito'),
]

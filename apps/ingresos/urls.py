# apps/usuarios/urls.py
# from django.urls import path
# from .views import test_view

# urlpatterns = [
    # path('test/', test_view),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_remitos, name='listar_remitos'),
    path('nuevo/', views.crear_remito, name='crear_remito'),
    path('editar/<int:pk>/', views.editar_remito, name='editar_remito'),
    path('eliminar/<int:pk>/', views.eliminar_remito, name='eliminar_remito'),
]

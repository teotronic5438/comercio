from django.urls import path
from . import views

urlpatterns = [
    path('pendientes/', views.ordenes_pendientes, name='ordenes_pendientes'),
    path('revisar/<int:orden_id>/', views.revisar_orden, name='revisar_orden'),  # vista siguiente
]

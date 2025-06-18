from django.urls import path
# from . import views
from .views import OrdenesPendientesListView, RevisarOrdenUpdateView, OrdenesActivasListView

urlpatterns = [
    # path('pendientes/', views.ordenes_pendientes, name='ordenes_pendientes'),
    # path('revisar/<int:orden_id>/', views.revisar_orden, name='revisar_orden'),
    path('pendientes/', OrdenesPendientesListView.as_view(), name='ordenes_pendientes'),
    path('revisar/<int:pk>/', RevisarOrdenUpdateView.as_view(), name='revisar_orden'),
    path('ordenes/activas/', OrdenesActivasListView.as_view(), name='ordenes_activas'),
]

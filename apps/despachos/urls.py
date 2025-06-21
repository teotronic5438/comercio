# apps/despachos/urls.py

from django.urls import path
from . import views

app_name = 'despachos' # Muy importante para los {% url %} tags

urlpatterns = [
    # URL para la vista de órdenes revisadas (punto de partida)
    path('revisadas/', views.OrdenesRevisadasView.as_view(), name='ordenes_revisadas'),

    # URLs para las nuevas vistas filtradas por destino
    path('nuevas/', views.OrdenesNuevasView.as_view(), name='ordenes_nuevas'),
    path('averiadas/', views.OrdenesAveriadasView.as_view(), name='ordenes_averiadas'),
    path('destruidas/', views.OrdenesDestruidasView.as_view(), name='ordenes_destruccion'), # Nota: 'destruccion' en singular por consistencia con tus clases

    # URL para procesar el despacho de órdenes (cambio de destino)
    # ¡AQUÍ ES DONDE AÑADIMOS EL NAME CORRECTO!
    path('procesar_despacho/', views.ProcesarDespachoOrdenesView.as_view(), name='procesar_despacho_ordenes'),

    # URL para armar pallets (si ya la tienes definida)
    # path('armar_pallet/', views.ArmarPalletView.as_view(), name='armar_pallet'), # Si tienes esta vista, asegúrate que esté aquí
]
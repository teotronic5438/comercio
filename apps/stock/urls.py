# from django.urls import path
# from .views import stock

# urlpatterns=[
#     path('stock/', stock, name="stock"),
#     # path('deposito/',stock_deposito, name="deposito"),
# ]

from django.urls import path
from .views import StockView

urlpatterns = [
    path('stock/', StockView.as_view(), name="stock"),
    # path('deposito/', stock_deposito, name="deposito"),
]
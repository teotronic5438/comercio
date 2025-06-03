from django.urls import path
from .views import stock, stock_deposito

urlpatterns=[
    path('stock/', stock, name="stock"),
    path('deposito/',stock_deposito, name="deposito"),
]
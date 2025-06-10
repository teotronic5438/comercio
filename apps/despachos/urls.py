# apps/despachos/urls.py

from django.urls import path
from . import views 

app_name = 'despachos' 

urlpatterns = [
    path('revisados/', views.ordenes_revisadas, name='ordenes_revisadas'),
]

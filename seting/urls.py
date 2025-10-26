"""
URL configuration for seting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/usuarios/login/', permanent=False)),
    path('usuarios/', include('apps.usuarios.urls', 'usuarios')),
    path('admin/', admin.site.urls),
    path('core/', include('apps.core.urls', namespace='core')),
    path('stock/', include('apps.stock.urls')),
    path('ingresos/', include('apps.ingresos.urls')),
    path('ingresos/history/', include('apps.ingresos.urls')),
    path("ordenes/", include('apps.ordenes.urls')),
    path('despachos/', include('apps.despachos.urls')),
    # path('api/ingresos/', include('apps.ingresos.urls')),
    
]

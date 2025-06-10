from django.urls import path
from .views import login, dashboard, logout
from django.urls import path, include

urlpatterns = [
    path('', login, name='Login'),
    path('dashboard/', dashboard, name='Dashboard'),
    path('logout/', logout, name='Logout'),
]

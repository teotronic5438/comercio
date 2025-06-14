from django.urls import path
from .views import dashboard,  home

""" 
    logout y login se hacen desde usuarios  ir a usuarios/urls.py
"""
app_name = 'core'
urlpatterns = [
   # path('', login, name='Login'),
    path('dashboard/', dashboard, name='Dashboard'),
    #path('logout/', logout, name='Logout'), BORRADO xq se accede desde usuarios:logout
    path('', home, name ='home'),
]

from django.urls import path
from .views import dashboard,  home, DashboardOrdenesView

""" 
    logout y login se hacen desde usuarios  ir a usuarios/urls.py
"""
app_name = 'core'
urlpatterns = [
   # path('', login, name='Login'),
    # path('dashboard/', dashboard, name='Dashboard'),
    #path('logout/', logout, name='Logout'), BORRADO xq se accede desde usuarios:logout
    # path('', home, name ='home'),
    # path('dashboard-ordenes/', DashboardOrdenesView.as_view(), name='dashboard_ordenes'),
    path('dashboard/', DashboardOrdenesView.as_view(), name='dashboard_ordenes'),
]

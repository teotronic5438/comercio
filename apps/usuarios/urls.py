from django.urls import path, include
#from django.contrib.auth.decorators import login_required
from .views import  LogoutUsuarioView,  RegistrarUsuario, login_view #, Login


app_name = 'usuarios'
urlpatterns = [
 
    path('register/',  RegistrarUsuario.as_view(), name ='register'),
    #path('accounts/login/',  Login.as_view(), name ='login'), #si usamos Login como clase template 
    path('login/',  login_view, name ='login'), 
    #path('logout/',  login_required(logoutUsuario) , name ='logout'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    
    

]
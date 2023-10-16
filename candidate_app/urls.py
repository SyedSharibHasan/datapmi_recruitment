from django.urls import path
from .views import welcome,signup,signin,user,admin



urlpatterns = [
    path('user/',user,name='user'),
    path('admin_page/',admin,name='admin'),
    path('signup/',signup,name='signup'),
    path('',signin,name='login'),
   
    
    ]















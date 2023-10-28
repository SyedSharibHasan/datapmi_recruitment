from django.urls import path
from .views import signup,signin,user,admin,Createcandidate



urlpatterns = [
    path('user/',user,name='user'),
    path('admin_page/',admin,name='admin'),
    path('signup/',signup,name='signup'),
    path('',signin,name='login'),
    path('create/',Createcandidate.as_view(),name='create')
    
    ]















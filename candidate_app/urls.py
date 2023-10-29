from django.urls import path
from .views import signup,signin,user,admin,Createcandidate,Detailcandidate,Deletecandidate,Updatecandidate,signout



urlpatterns = [
    path('user/',user,name='user'),   ## listed candidates
    path('admin_page/',admin,name='admin'),   ## page only for admin
    path('signup/',signup,name='signup'),
    path('',signin,name='login'),
    path('create/',Createcandidate.as_view(),name='create'),   ## create each acndidate
    path('detail/<int:pk>/',Detailcandidate.as_view(),name='detail'),   ## details of each candidate
    path('delete/<int:pk>/',Deletecandidate.as_view(),name='delete') ,  ## delete  a candidate
    path('update/<int:pk>/',Updatecandidate.as_view(),name='update') ,  ## update a candidate
    
    path("signout/", signout, name='signout'),
    ]















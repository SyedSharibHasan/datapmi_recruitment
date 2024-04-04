from django.urls import path
from .views import signin,signup,admin,user_control,signout,account,Edit_account,manage_account,email_change_otp
from . import views



urlpatterns = [
    path('signup/',signup,name='signup'),
    path('verify_otp/', views.verify_otp, name='verify_otp'), 
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('profile/',account,name='profile'), 
    path('edit_account/<int:pk>/', Edit_account.as_view(), name='edit_account'),
    path('email_change_otp/', email_change_otp, name='email_change_otp'),
    path('manage_account/<str:action>/', views.manage_account, name='manage_account'),
    path('admin_page/',admin,name='admin'), 
    path('user_control/<int:pk>/', user_control, name='user_control'), 
    

    ### Always kept at last
    path("signout/", views.signout, name='signout'),
    path('<str:action>/',signin,name='login'),
    path('', views.signin, {'action': 'login'}, name='login_default'), 

]








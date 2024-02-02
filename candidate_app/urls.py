from django.urls import path
from .views import signup,signin,user,admin,ListCandidate,Createcandidate,Detailcandidate,delete_candidate,Updatecandidate,signout,Allcandidates,dashboard,account,autocomplete_username,Filter,autocomplete_skills,all_filter,autocomplete_locations,mycandidates_count,selected_candidates,rejected_candidates,inprogress_candidates,list_of_candidates,Edit_account,manage_account,totalcandidates_count,saved_candidates,verify_otp,reset_password,get_skills
from . import views



urlpatterns = [
    path('user/',user,name='user'),   
    path('admin_page/',admin,name='admin'),   
    path('signup/',signup,name='signup'),
    path('list/',ListCandidate.as_view(),name='list'),   
    path('create/',Createcandidate.as_view(),name='create'),  
    path('detail/<int:pk>/',Detailcandidate.as_view(),name='detail'),   
    path('delete/<int:pk>/',delete_candidate,name='delete') , 
    path('update/<int:pk>/',Updatecandidate.as_view(),name='update') ,  
    path('all/',Allcandidates.as_view(),name='all'), 
    path('dashboard/',dashboard,name='dashboard'),
    path('profile/',account,name='profile'), 
    path('edit_account/<int:pk>/', Edit_account.as_view(), name='edit_account'),
    path('filter/', Filter.as_view(), name='filter'),
    path('autocomplete-username/', autocomplete_username, name='autocomplete_username'),
    path('autocomplete-skills/', autocomplete_skills, name='autocomplete_skills'),
    path('autocomplete-locations/', autocomplete_locations, name='autocomplete_locations'),
    path('all_filter/', all_filter, name='all_filter'),
    path('mycandidates_count', mycandidates_count, name='mycandidates_count'),
    path('selected_candidates', selected_candidates, name='selected_candidates'),
    path('rejected_candidates', rejected_candidates, name='rejected_candidates'),
    path('inprogress_candidates', inprogress_candidates, name='inprogress_candidates'),
    path('allcandidates_count', totalcandidates_count, name='allcandidates_count'),
    path('savedcandidates_count', saved_candidates, name='savedcandidates_count'),
    path('list_of_candidates/<str:status>/', list_of_candidates, name='list_of_candidates'),
    path('manage_account/<str:action>/', views.manage_account, name='manage_account'),
    path('verify_otp/', views.verify_otp, name='verify_otp'), 
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('get_skills_api/', get_skills, name='get_skills_api'),

    path("signout/", signout, name='signout'),
    path('<str:action>/',signin,name='login'),
    path('', views.signin, {'action': 'login'}, name='login_default'), 
         
]

























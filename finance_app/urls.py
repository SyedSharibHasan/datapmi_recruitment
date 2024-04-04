from django.urls import path
from .views import add_employee,active_inactive,Updateemployee,finance_dashboard,all_employee,detail_employee,delete_employee,end_work_order,export_selected_to_excel


urlpatterns = [
    path("add_employee/", add_employee, name='add_employee'),
    path("all_employee/", all_employee, name='all_employee'),
    path("active_inactive/<str:action>/", active_inactive, name='active_inactive'),
    path('update_employee/<int:pk>/',Updateemployee.as_view(),name='update_employee'), 
    path("finance_dashboard/", finance_dashboard, name='finance_dashboard'),
   
    path("detail_employee/<int:pk>/", detail_employee, name='detail_employee'),
    path("delete_employee/<int:pk>/", delete_employee, name='delete_employee'),
    path("end_work_order/", end_work_order, name='end_work_order'),
    path('export_selected_to_excel/',export_selected_to_excel,name='export_selected_to_excel'),
]










from django.db import models
from candidate_app.models import CustomUser





##### Finance team
class Employee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=150, null=True, blank=True)
    alt_mobile = models.CharField(max_length=150, null=True, blank=True)
    position = models.CharField(max_length=150, null=True, blank=True)
    client_name = models.CharField(max_length=150, null=True, blank=True)
    client_location = models.CharField(max_length=150, null=True, blank=True)
    project_director = models.CharField(max_length=150, null=True, blank=True)
    project_partner = models.CharField(max_length=150, null=True, blank=True)
    fees = models.CharField(max_length=150,null=True, blank=True)
    employee_status = models.CharField(max_length=20, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    last_working_date = models.DateField(null=True, blank=True)
    start_date_of_work_order = models.DateField(null=True, blank=True)
    end_date_of_work_order = models.DateField(null=True, blank=True)
    work_order_detail = models.CharField(max_length=150, null=True, blank=True)
    upload_work_order = models.FileField(upload_to='work_order/', null=True, blank=True)
    upload_nda = models.FileField(upload_to='nda/', null=True, blank=True)
    upload_resume = models.FileField(upload_to='employeeresume/', null=True, blank=True)
    active_inactive = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-created"]


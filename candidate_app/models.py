from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='image/', max_length=400, blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_token_expiration = models.DateTimeField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True, verbose_name='Join Date',null=True)
    role = models.CharField(max_length=255,null=False)                     ######## Fianance or Recruiter



class Skill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Candidate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    client_name = models.CharField(max_length=15)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150)
    mode_of_work = models.CharField(max_length=150, default='full_time',null=True)
    gender = models.CharField(max_length=50, default='unknown', null=True,blank=True)
    college = models.CharField(max_length=50,    null=True,blank=True)
    graduation_year= models.CharField(max_length=50, null=True,blank=True)
    qualification = models.TextField(null=True,blank=True)
    skills = models.ManyToManyField(Skill)  
    experience = models.FloatField(null=True, blank=True)
    relevent_experience = models.FloatField(null=True, blank=True)
    designation = models.CharField(max_length=50, null=True,blank=True)
    expected_ctc = models.CharField(max_length=50, null=True,blank=True)
    current_ctc = models.CharField(max_length=50, null=True,blank=True)
    offer_in_hands = models.CharField(max_length=50,default=None, null=True,blank=True)
    offer_details= models.CharField(max_length=50,default=None, null=True,blank=True)     ###  hidden box
    notice_period = models.CharField(max_length=50, null=True,blank=True)
    current_company = models.CharField(max_length=100, null=True,blank=True)
    reason_for_change = models.CharField(max_length=2000, null=True,blank=True)          ###  hidden
    location = models.CharField(max_length=50, null=True,blank=True)
    resume = models.FileField(upload_to='resume/',max_length=200,blank=True,null=True)
    remarks = models.TextField(null=True,blank=True)
    updated_by = models.CharField(max_length=50, null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    screening_time = models.CharField(max_length=100, null=True,blank=True)
    recruiter = models.CharField(max_length=50, null=True,blank=True)
    status = models.CharField(max_length=100, null=True,blank=True)
    rejection_reason = models.CharField(max_length=100, null=True,blank=True)         ### hidden 
    additional_status = models.CharField(max_length=100, null=True,blank=True)
    rejection_reason_for_r1_r4 = models.CharField(max_length=100, null=True,blank=True)        ## hidden 
    offer = models.CharField(max_length=100, null=True,blank=True)
    offer_reject_reason = models.CharField(max_length=100, null=True,blank=True)
    
    def __str__(self):
        return self.email


    class Meta:
        ordering = ["-updated_on"]

    def formatted_updated_on(self):
        updated_on_timezone = timezone.localtime(self.updated_on, timezone=timezone.get_current_timezone())

        # Format the datetime
        return updated_on_timezone.strftime('%d/%b/%Y %I:%M %p')


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










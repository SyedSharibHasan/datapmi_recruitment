from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from account_app.models import CustomUser


# class CustomUser(AbstractUser):
#     contact = models.CharField(max_length=15, blank=True, null=True)
#     image = models.ImageField(upload_to='image/', max_length=400, blank=True, null=True)
#     password_reset_token = models.CharField(max_length=255, null=True, blank=True)
#     password_reset_token_expiration = models.DateTimeField(null=True, blank=True)
#     join_date = models.DateTimeField(auto_now_add=True, verbose_name='Join Date',null=True)
#     role = models.CharField(max_length=255,null=False)                     ######## Fianance or Recruiter



class Skill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Candidate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(default='',unique=True)
    phone = models.CharField(default='',max_length=500)
    client_name = models.CharField(default='',max_length=500)
    date_of_excel = models.CharField(default='',max_length=500)
    due_date = models.CharField(max_length=500, default='',null=True)
    candidate_name = models.CharField(max_length=600, null=True) 
    mode_of_work = models.CharField(max_length=500, default='',null=True)
    gender = models.CharField(max_length=300, default='', null=True,blank=True)
    college = models.CharField(max_length=1000, null=True,blank=True)
    graduation_year= models.CharField(default='',max_length=300, null=True,blank=True)
    qualification = models.TextField(default='',null=True,blank=True)
    skills = models.ManyToManyField(Skill)  
    experience = models.FloatField(null=True,blank=True,default=None)
    relevent_experience = models.FloatField(null=True, blank=True,default=None)
    designation = models.CharField(default='',max_length=500, null=True,blank=True)
    expected_ctc = models.CharField(max_length=255, null=True,blank=True,default='')
    current_ctc = models.CharField(max_length=255, null=True,blank=True,default='')
    offer_in_hands = models.CharField(max_length=1000, null=True,blank=True,default='')  
    offer_details= models.CharField(max_length=500, null=True,blank=True,default='')     ###  not used
    notice_period = models.CharField(max_length=1500, null=True,blank=True,default='')
    current_company = models.CharField(max_length=700, null=True,blank=True,default='')
    reason_for_change = models.CharField(max_length=700, null=True,blank=True,default='')            ### not used       
    location = models.CharField(max_length=500, null=True,blank=True,default='')
    resume = models.FileField(upload_to='resume/',max_length=800,blank=True,null=True)
    remarks = models.TextField(null=True,blank=True,default='')
    updated_by = models.CharField(max_length=600, null=True,blank=True,default='Not entered')
    updated_on = models.DateTimeField(auto_now=True, null=True)
    screening_time = models.CharField(max_length=400, null=True,blank=True,default='')            ###   not used
    recruiter = models.CharField(max_length=600, null=True,blank=True)
    status = models.CharField(max_length=600, null=True,blank=True,default='')
    rejection_reason = models.CharField(max_length=100, null=True,blank=True,default='')        
    additional_status = models.CharField(max_length=100, null=True,blank=True,default='')                   ### not used
    rejection_reason_for_r1_r4 = models.CharField(max_length=100, null=True,blank=True,default='')        ## not used



    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-updated_on"]

    def formatted_updated_on(self):
        updated_on_timezone = timezone.localtime(self.updated_on, timezone=timezone.get_current_timezone())

        # Format the datetime
        return updated_on_timezone.strftime('%d/%b/%Y %I:%M %p')
    
  


# ##### Finance team
     
# class Employee(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=150, null=True, blank=True)
#     email = models.EmailField(unique=True)
#     mobile = models.CharField(max_length=150, null=True, blank=True)
#     alt_mobile = models.CharField(max_length=150, null=True, blank=True)
#     position = models.CharField(max_length=150, null=True, blank=True)
#     client_name = models.CharField(max_length=150, null=True, blank=True)
#     client_location = models.CharField(max_length=150, null=True, blank=True)
#     project_director = models.CharField(max_length=150, null=True, blank=True)
#     project_partner = models.CharField(max_length=150, null=True, blank=True)
#     fees = models.CharField(max_length=150,null=True, blank=True)
#     employee_status = models.CharField(max_length=20, null=True, blank=True)
#     joining_date = models.DateField(null=True, blank=True)
#     last_working_date = models.DateField(null=True, blank=True)
#     start_date_of_work_order = models.DateField(null=True, blank=True)
#     end_date_of_work_order = models.DateField(null=True, blank=True)
#     work_order_detail = models.CharField(max_length=150, null=True, blank=True)
#     upload_work_order = models.FileField(upload_to='work_order/', null=True, blank=True)
#     upload_nda = models.FileField(upload_to='nda/', null=True, blank=True)
#     upload_resume = models.FileField(upload_to='employeeresume/', null=True, blank=True)
#     active_inactive = models.CharField(max_length=20, null=True, blank=True)
#     created = models.DateTimeField(auto_now=True, null=True)

#     def __str__(self):
#         return self.email

#     class Meta:
#         ordering = ["-created"]









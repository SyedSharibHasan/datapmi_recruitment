from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models




class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)


class Skill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Candidate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    client_name = models.CharField(max_length=15)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150)
    mode_of_work = models.CharField(max_length=150, default='full_time',null=True)

    gender = models.CharField(max_length=50, default='unknown', null=True,blank=True)
    college = models.CharField(max_length=50, null=True,blank=True)
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
    updated_on = models.DateTimeField(auto_now_add=True, null=True)
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








class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/',max_length=400,blank=True)








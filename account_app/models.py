from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='image/', max_length=400, blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_token_expiration = models.DateTimeField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True, verbose_name='Join Date',null=True)
    role = models.CharField(max_length=255,null=False)                     ######## Fianance or Recruiter









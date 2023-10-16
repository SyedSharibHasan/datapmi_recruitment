from django.db import models

# Create your models here.
class Candidte(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150)
    alt_phone = models.CharField(max_length=15)
    dob = models.DateField()
    sex = models.CharField(max_length=50)
    qualification = models.TextField()
    skills = models.TextField()
    experience = models.IntegerField()
    designation = models.CharField(max_length=50)
    expected_ctc = models.FloatField()
    current_ctc = models.FloatField()
    availability = models.BooleanField(default=True)
    notice_period = models.IntegerField()
    current_company = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    resume = models.FileField(upload_to='static/resumes/')
    remarks = models.TextField()
    updated_by = models.CharField(max_length=50)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
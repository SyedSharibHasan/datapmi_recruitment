from django.db import models


class Candidate(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150)
    alt_phone = models.CharField(max_length=15)
    # dob = models.DateField(null=True)
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
    resume = models.FileField(upload_to='resume/',max_length=200,blank=True)
    remarks = models.TextField()
    updated_by = models.CharField(max_length=50)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email










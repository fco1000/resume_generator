# Create your models here.
# resumes/models.py
from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15,null=True)
    education = models.TextField(null=True)
    experience = models.TextField(null=True)
    skills = models.TextField(null=True)

    def __str__(self):
        return f'{self.user}\'s resume'
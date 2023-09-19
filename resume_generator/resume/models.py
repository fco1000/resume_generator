# Create your models here.
# resumes/models.py
from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15,null=True)
    education = models.TextField(null=True,help_text="Enter all the levels of educations you've been through along with the dates from last(most recent) to first(beginning of your education) each with their respective achievements")
    experience = models.TextField(null=True,help_text="Enter the experiences you have in the various jobs you've done along with the titles you held in the respective jobs.(From current to first)")
    skills = models.TextField(null=True,help_text="Enter the skills you have")
    html_content = models.TextField(blank=True, null=True, editable=False)

    def __str__(self):
        return f'{self.user}\'s resume'
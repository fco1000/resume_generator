# resumes/forms.py
from django import forms
from .models import Resume
from django.contrib.auth.models import User

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'email', 'phone_number', 'education', 'experience','skills']

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
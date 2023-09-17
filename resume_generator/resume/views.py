# Create your views here.
# resumes/views.py
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from .forms import ResumeForm,UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView

from django.contrib.auth.decorators import login_required
from resume_generator import settings
from .models import *

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def createUser(request):
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
    else:
        return render(request, 'user/sign_up.html',{'form':form})
    
class userLoginView(LoginView):
    template_name = 'user/login_user.html'
    
    def get_success_url(self):
        return reverse('home') 
        
class userLogoutView(LoginRequiredMixin,LogoutView):    
    def get_success_url(self):
        return reverse('login') 

def homeView(request):
    return render(request,'resume/home.html')

@login_required(login_url=settings.LOGIN_URL)
def generate_resume(request):
    form =ResumeForm()
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save()
            reverse('')
    else:
        return render(request, 'resume/generate_resume.html', {'form': form})
    
@login_required(login_url=settings.LOGIN_URL)
def update_resume(request,id):
    resume = Resume.objects.get(id=id)
    form =ResumeForm(instance=resume)
    if request.method == 'POST':
        form = ResumeForm(request.POST,instance=resume)
        if form.is_valid():
            form.save()
            reverse('')
    else:
        return render(request, 'resume/update_resume.html', {'form': form})
    
@login_required(login_url=settings.LOGIN_URL)    
def view_resume(request):
    user = request.user
    resume = Resume.objects.get(user=user)
    if resume is None:
        reverse('resumeCreate')
    else:
        return render(request, 'resume/resume_showcase.html',{'resume',resume})




def generate_pdf(request, id):
    # Get the resume data from the database (replace with your logic)
    resume = Resume.objects.get(pk=id)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.name}_resume.pdf"'

    # Create the PDF content using ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Resume")
    p.drawString(100, 730, f"full_name: {resume.full_name}")
    p.drawString(100, 710, f"email: {resume.email}")
    p.drawString(100, 710, f"phone_number: {resume.phone_number}")
    p.drawString(100, 710, f"education: {resume.education}")
    p.drawString(100, 710, f"experience: {resume.experience}")
    p.drawString(100, 710, f"skills: {resume.skills}")    

    # Save the PDF
    p.showPage()
    p.save()
    
    return response

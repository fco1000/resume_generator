# Create your views here.
# resumes/views.py
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import ResumeForm,UserCreationForm,AccountsResumeForm
from .utils import render_to_pdf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required
from resume_generator import settings
from .models import Resume,AccountsResume
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.models import User

def createUser(request):
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user=form.save()
            user.save()
            # Log the user in
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'user/sign_up.html',{'form':form})

class userLoginView(LoginView):
    template_name = 'user/login_user.html'

    def get_success_url(self):
        return reverse('home')
    
def user_view(request):
    user = request.user.username
    users = User.objects.get(username=user)
    return render(request, 'user/user.html', {'users':users})

class userLogoutView(LoginRequiredMixin,LogoutView):
    def get_success_url(self):
        return reverse('login')

def homeView(request):
    user = request.user
    try:
        resumes = AccountsResume.objects.get(user=user)
    except:
        resumes = None
    return render(request,'resume/home.html' ,{'resumes':resumes})


def generate_resume(request):
    form1 = ResumeForm()
    form2 = AccountsResumeForm()
    user = request.user
    
    if user.is_authenticated:
        if request.method == 'POST':
            form2 = AccountsResumeForm(request.POST)
            if form2.is_valid():
                Resume = form2.save(commit=False)
                Resume.user = user
                Resume.save()
                Resume.html_content = form2.cleaned_data.get('html_content')

                Resume.save()
                print(Resume.full_name)
                return redirect('resumeView', resume_id=Resume.id)  # Specify the resume_id
    else:
        if request.method == 'POST':
            form1 = ResumeForm(request.POST)
            if form1.is_valid():
                resume = form1.save(commit=False)
                resume.html_content = form1.cleaned_data.get('html_content')
                resume.save()
                return redirect('resumeView', resume_id=resume.id)  # Specify the resume_id
    return render(request, 'resume/generate_resume.html', {'form1': form1, 'form2': form2})



def view_resume(request, resume_id):
    user = request.user
    
    if user.is_authenticated:
        try:
            resume = AccountsResume.objects.get(user=user)
            return render(request, 'resume/resume_showcase.html', {'resume': resume})
        except AccountsResume.DoesNotExist:
            return redirect('resumeCreate')  # Redirect to create the resume for authenticated users
    else:
        try:
            resume = Resume.objects.get(id=resume_id)
            return render(request, 'resume/resume_showcase.html', {'resume': resume})
        except Resume.DoesNotExist:
            return redirect('resumeCreate')  # Redirect to create the resume for non-authenticated users
    
# @login_required(login_url=settings.LOGIN_URL)
def update_resume(request,id):
    resume = Resume.objects.get(id=id)
    form =ResumeForm(instance=resume)
    if request.method == 'POST':
        form = ResumeForm(request.POST,instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resumeView')
    else:
        return render(request, 'resume/update_resume.html', {'form': form})


class GeneratePdf(View):
    def get(self, request,resume_id,pdf_rendering='false', *args, **kwargs):
        # Get the user associated with the current request
        user = request.user
        
        try:
            # Fetch the user's resume data from the Resume model
            if user.is_authenticated:
                resume = AccountsResume.objects.get(user=user)
            else:
                resume = Resume.objects.get(id=resume_id)

            pdf_rendering = pdf_rendering.lower() == 'true'
            # Create a context dictionary with resume data
            context = {
                "resume": resume,
                "pdf_rendering": pdf_rendering,
            }

            # Generate the PDF using the context data and the 'resume_showcase.html' template
            pdf = render_to_pdf('resume/resume_showcase.html', context)

            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = f"Resume_for_{resume.full_name}.pdf"
                content = f"inline; filename={filename}"
                response['Content-Disposition'] = content
                return response
        except AccountsResume.DoesNotExist:
            return HttpResponse("Resume not found for the current user.", status=404)
        
# Create your views here.
# resumes/views.py
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import ResumeForm,UserCreationForm
from .utils import render_to_pdf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required
from resume_generator import settings
from .models import Resume
from django.views import View
from django.contrib.auth import login

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

class userLogoutView(LoginRequiredMixin,LogoutView):
    def get_success_url(self):
        return reverse('login')

def homeView(request):
    return render(request,'resume/home.html')

@login_required
@login_required
def generate_resume(request):
    form = ResumeForm()
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            resume.html_content = form.cleaned_data.get('html_content')

            resume.save()
            return redirect('resumeView')
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
            return redirect('resumeView')
    else:
        return render(request, 'resume/update_resume.html', {'form': form})

def view_resume(request):
    user = request.user
    resume = Resume.objects.get(user=user)
    if resume is None:
        reverse('resumeCreate')
    else:
        return render(request, 'resume/resume_showcase.html',{'resume':resume})

class GeneratePdf(View):
    def get(self, request,pdf_rendering='false', *args, **kwargs):
        # Get the user associated with the current request
        user = request.user

        try:
            # Fetch the user's resume data from the Resume model
            resume = Resume.objects.get(user=user)

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
        except Resume.DoesNotExist:
            return HttpResponse("Resume not found for the current user.", status=404)

        return HttpResponse("Page Not Found", status=404)

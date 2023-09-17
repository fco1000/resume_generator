from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('account_create/',createUser,name='signup'),    
    path('login/',userLoginView.as_view(),name='login'),
    path('logout/',userLogoutView.as_view(),name='logout'),
    
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html'),name='password_reset'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name='user/password_change_form.html'), name="password_change"),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),name="password_change_done"),
    
    path('',homeView, name='home'),
    path('create-resume/',generate_resume,name='resumeCreate'),
    path('update_resume/<int:id>',update_resume,name='resumeUpdate'),
    path('resume/',view_resume,name='resumeView'),
    path('generate_pdf/<int:resume_id>/', generate_pdf, name='generate_pdf'),
    
]
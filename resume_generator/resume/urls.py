from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('account_create/',views.createUser,name='signup'),
    path('login/',views.userLoginView.as_view(),name='login'),
    path('logout/',views.userLogoutView.as_view(),name='logout'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html',from_email='fco1000djangodev@gmail.com'),name='password_reset'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name='user/password_change_form.html'), name="password_change"),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),name="password_change_done"),

    path('',views.homeView, name='home'),
    path('create-resume/',views.generate_resume,name='resumeCreate'),
    path('update_resume/<int:id>',views.update_resume,name='resumeUpdate'),
    path('resume/',views.view_resume,name='resumeView'),
    path('generate_pdf/<int:id>/<str:pdf_rendering>/', views.GeneratePdf.as_view(), name='generate_pdf'),

]
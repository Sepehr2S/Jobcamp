# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('freelancer/dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('employer/profile/', views.employer_profile_view, name='employer_profile'),
    path('employer/edit-profile/', views.edit_employer_profile, name='edit_employer_profile'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('employer/applicant/<int:application_id>/', views.applicant_profile, name='applicant_profile'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('application/<int:application_id>/reject/', views.reject_application, name='reject_application'),
]
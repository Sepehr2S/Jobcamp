from django.urls import path
from . import views

urlpatterns = [
    path('signup/freelancer/', views.freelancer_signup, name='freelancer_signup'),
    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('dashboard/freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
]
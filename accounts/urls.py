# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('freelancer/dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path("accounts/profile/edit/", views.edit_profile, name="edit_profile"),
    path('logout/', views.logout_view, name='logout'),
]

from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, FreelancerSignUpForm, EmployerSignUpForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # بعداً مسیر لاگین رو درست می‌کنیم
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def freelancer_signup(request):
    if request.method == 'POST':
        form = FreelancerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('freelancer_dashboard')  # بعداً این صفحه رو می‌سازیم
    else:
        form = FreelancerSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'title': 'ثبت‌نام فریلنسر'})

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('employer_dashboard')
    else:
        form = EmployerSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'title': 'ثبت‌نام کارفرما'})


@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return HttpResponseForbidden("شما اجازه دسترسی به این صفحه را ندارید.")
    return render(request, 'candidate-profile-main.html')  # داشبورد کاربر (فریلنسر)

@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':
        return HttpResponseForbidden("شما اجازه دسترسی به این صفحه را ندارید.")
    return render(request, 'dashboard-main.html')  # داشبورد کارفرما
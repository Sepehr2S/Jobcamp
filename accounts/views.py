from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Profile
from .forms import SignUpForm, CustomLoginForm

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            user.role = role  # ذخیره نقش کاربر
            user.save()
            Profile.objects.create(user=user)
            messages.success(request, "ثبت‌نام با موفقیت انجام شد. حالا می‌توانید وارد شوید.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user = authenticate(request, username=username, password=password)

            if user is not None and user.role == role:
                login(request, user)
                messages.success(request, f"خوش آمدید {user.username} ({role})")
                return redirect('dashboard')  # می‌تونی تغییر بدی به صفحه اصلی
            else:
                messages.error(request, "نام کاربری، رمز یا نقش اشتباه است.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return redirect('home')
    return render(request, 'candidate-profile-main.html')

@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':
        return redirect('home')
    return render(request, 'dashboard-main.html')

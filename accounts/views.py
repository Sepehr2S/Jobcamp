from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from .models import Profile
from .forms import SignUpForm, CustomLoginForm, UserForm, ProfileForm

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

                if user.role == 'freelancer':
                    return redirect('freelancer_dashboard')
                elif user.role == 'employer':
                    return redirect('employer_dashboard')

            else:
                messages.error(request, "نام کاربری، رمز یا نقش اشتباه است.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return redirect('home')

    profile = get_object_or_404(Profile, user=request.user)
    skills = profile.get_skills_list()  # استفاده از متد جدید
    experiences = profile.experiences.all()

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)

    context = {
        "profile": profile,
        "skills": skills,
        "experiences": experiences,
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/candidate-profile-main.html", context)


@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':
        return redirect('home')
    return render(request, 'dashboard-main.html')


@login_required
def edit_profile(request):
    if request.user.role != 'freelancer':
        return redirect('home')

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "پروفایل شما با موفقیت بروزرسانی شد.")
            return redirect('freelancer_dashboard')
        else:
            print("UserForm errors:", user_form.errors)
            print("ProfileForm errors:", profile_form.errors)
            messages.error(request, "خطایی در فرم وجود دارد. لطفاً بررسی کنید.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "شما با موفقیت از سیستم خارج شدید.")
    return redirect('login')
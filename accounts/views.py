from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Profile, EmployerProfile, Job, Application
from .forms import SignUpForm, CustomLoginForm, UserForm, ProfileForm, EmployerProfileForm, JobForm

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            user.role = role
            user.save()
            if role == 'freelancer':
                Profile.objects.create(user=user)
            elif role == 'employer':
                EmployerProfile.objects.create(user=user, company_name=user.username)
            messages.success(request, "ثبت‌نام با موفقیت انجام شد. حالا می‌توانید وارد شوید.")
            return redirect('accounts:login')
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
                    return redirect('accounts:freelancer_dashboard')
                elif user.role == 'employer':
                    return redirect('accounts:employer_dashboard')
            else:
                messages.error(request, "نام کاربری، رمز یا نقش اشتباه است.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return redirect('website:home')
    profile = get_object_or_404(Profile, user=request.user)
    skills = profile.get_skills_list()
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
        return redirect('website:home')
    profile = get_object_or_404(EmployerProfile, user=request.user)
    jobs = Job.objects.filter(employer=request.user, is_active=True)
    applications = Application.objects.filter(job__employer=request.user)
    context = {
        'profile': profile,
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'accounts/employer_dashboard.html', context)

@login_required
def edit_profile(request):
    if request.user.role != 'freelancer':
        return redirect('website:home')
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "پروفایل شما با موفقیت بروزرسانی شد.")
            return redirect('accounts:freelancer_dashboard')
        else:
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
    return redirect('accounts:login')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/candidate-profile-main.html'
    success_url = reverse_lazy('accounts:freelancer_dashboard')

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    context = {'job': job}
    return render(request, 'accounts/job_detail.html', context)

@login_required
def edit_job(request, job_id):
    if request.user.role != 'employer':
        return redirect('website:home')
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "آگهی شغلی با موفقیت ویرایش شد.")
            return redirect('accounts:employer_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'accounts/edit_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    if request.user.role != 'employer':
        return redirect('website:home')
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "آگهی شغلی با موفقیت حذف شد.")
        return redirect('accounts:employer_dashboard')
    return render(request, 'accounts/confirm_delete_job.html', {'job': job})

@login_required
def reject_application(request, application_id):
    if request.user.role != 'employer':
        return redirect('website:home')
    application = get_object_or_404(Application, id=application_id, job__employer=request.user)
    if request.method == 'POST':
        application.status = 'rejected'
        application.save()
        messages.success(request, "درخواست با موفقیت رد شد.")
        return redirect('accounts:employer_dashboard')
    return render(request, 'accounts/confirm_reject_application.html', {'application': application})

@login_required
def edit_employer_profile(request):
    if request.user.role != 'employer':
        return redirect('website:home')
    profile, created = EmployerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل شرکت با موفقیت بروزرسانی شد.")
            return redirect('accounts:employer_profile')
        else:
            messages.error(request, "خطایی در فرم وجود دارد. لطفاً بررسی کنید.")
    else:
        form = EmployerProfileForm(instance=profile)
    return render(request, 'accounts/edit_employer_profile.html', {'form': form})

@login_required
def post_job(request):
    if request.user.role != 'employer':
        return redirect('website:home')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "آگهی شغلی با موفقیت منتشر شد.")
            return redirect('accounts:employer_dashboard')
    else:
        form = JobForm()
    return render(request, 'accounts/post_job.html', {'form': form})

@login_required
def applicant_profile(request, application_id):
    if request.user.role != 'employer':
        return redirect('website:home')
    application = get_object_or_404(Application, id=application_id, job__employer=request.user)
    profile = get_object_or_404(Profile, user=application.applicant)
    context = {
        'application': application,
        'profile': profile,
        'skills': profile.get_skills_list(),
        'experiences': profile.experiences.all(),
    }
    return render(request, 'accounts/applicant_profile.html', context)

@login_required
def employer_profile_view(request):
    if request.user.role != 'employer':
        return redirect('website:home')
    profile = get_object_or_404(EmployerProfile, user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/employer_profile.html', context)
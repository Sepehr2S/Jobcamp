from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile, WorkExperience, EmployerProfile, Job


User = get_user_model()

ROLE_CHOICES = [
    ('freelancer', 'کارجو (Freelancer)'),
    ('employer', 'کارفرما (Employer)'),
]

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')


class CustomLoginForm(AuthenticationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'phone', 'skills']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مهارت‌ها را با کاما جدا کنید (مثال: پایتون, جنگو, جاوااسکریپت)'}),
        }


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['title']


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'logo', 'description', 'website', 'location', 'phone', 'company_type', 'founded_date', 'company_size']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'job_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }



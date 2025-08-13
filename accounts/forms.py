from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # پروفایل را به صورت دستی ایجاد می‌کنیم
            Profile.objects.create(user=user)
        return user

class FreelancerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'freelancer'
        if commit:
            user.save()
            Profile.objects.create(user=user)  # ایجاد پروفایل خالی
        return user


class EmployerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employer'
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user
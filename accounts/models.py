from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('freelancer', 'کارجو'),
        ('employer', 'کارفرما'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='freelancer')

    def __str__(self):
        return self.username

def default_profile_pic():
    return 'default/avatar.png'

def default_company_logo():
    return 'default/company_logo.png'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'freelancer'})
    avatar = models.ImageField(upload_to='avatars/', default=default_profile_pic)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)
    website = models.URLField(blank=True, null=True)  # اضافه شده برای هماهنگی با مودال

    def __str__(self):
        return f"{self.user.username} Profile"

    def get_skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company_size = models.CharField(max_length=50, blank=True)  # جدید: اندازه شرکت
    founded_date = models.CharField(max_length=10, blank=True)  # جدید: تاریخ تأسیس
    company_type = models.CharField(max_length=50, blank=True)  # جدید: نوع شرکت

    def __str__(self):
        return self.company_name

class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'})
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=(('full_time', 'تمام وقت'), ('part_time', 'پاره وقت')))
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'freelancer'})
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('pending', 'در انتظار'), ('accepted', 'پذیرفته شده'), ('rejected', 'رد شده')), default='pending')

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company or 'Unknown'}"
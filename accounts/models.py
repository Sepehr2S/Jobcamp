# accounts/models.py
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
    return 'default/avatar.png'  # مسیر داخل MEDIA


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default=default_profile_pic)
    bio = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

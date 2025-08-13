from django.urls import path
from website.views import *


app_name = 'website'

urlpatterns=[
    path('', home, name='home'),
    path('hello', hello, name='hello'),
    path('contact',contact, name="contact" ),
]

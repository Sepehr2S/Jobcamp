from django.shortcuts import render

# Create your views here.


def hello(request):
    return render(request, 'website/home-1.html')
from django.shortcuts import render
from website.forms import ContactForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render (request, "website/home-1.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Successfully Sent The Message!')
            form.save()
        else:
            messages.error(request, 'Please correct the errors below.')
    form = ContactForm()
    return render(request, "website/contact.html", {"form": form})

def hello(request):
    return render(request, 'website/contact.html')
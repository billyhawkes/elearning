from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, redirect, render

from .forms import RegisterForm

# Create your views here.


def home(request):
    return render(request, "home.html")


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/dashboard")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})


def dashboard(request):
    return render(request, "dashboard.html")

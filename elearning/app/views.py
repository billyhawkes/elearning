from django.contrib.auth import login, logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from .forms import CourseForm, RegisterForm
from .models import Course

# Create your views here.


def is_teacher(user):
    return user.groups.filter(name="teacher").exists()


def home(request):
    return render(request, "home.html")


def logoutUser(request):
    logout(request)
    return redirect("/login")


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_group = Group.objects.get(name=form.cleaned_data["group"])
            my_group.user_set.add(user)
            login(request, user)
            return redirect("/dashboard")
    else:
        form = RegisterForm()

    return render(request, "registration/sign_up.html", {"form": form})


@login_required(login_url="/login")
def dashboard(request):
    if is_teacher(request.user):
        courses = Course.objects.filter(teacher=request.user)
        return render(request, "dashboard/teacher.html", {"courses": courses})
    else:
        courses = Course.objects.all()
        return render(request, "dashboard/student.html", {"courses": courses})


@login_required(login_url="/login")
@permission_required("app.add_course", login_url="/login", raise_exception=True)
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect("/dashboard")
    else:
        form = CourseForm()
    return render(request, "create_course.html", {"form": form})

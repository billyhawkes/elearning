from django.contrib.auth import login, logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .forms import CourseForm, RegisterForm, SearchForm
from .models import Course, Notification

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
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:5]
    if is_teacher(request.user):
        courses = Course.objects.filter(teacher=request.user)
        return render(
            request,
            "dashboard/teacher.html",
            {"courses": courses, "notifications": notifications},
        )
    else:
        courses = Course.objects.exclude(students=request.user)
        enrolled_courses = Course.objects.filter(students=request.user)
        return render(
            request,
            "dashboard/student.html",
            {
                "courses": courses,
                "enrolled_courses": enrolled_courses,
                "notifications": notifications,
            },
        )


@login_required(login_url="/login")
@permission_required("app.add_course", login_url="/login", raise_exception=True)
def search(request):
    query = request.GET.get("query")
    users = []
    if query:
        users = User.objects.filter(username__icontains=query)
    return render(request, "dashboard/search.html", {"query": query, "results": users})


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


@login_required(login_url="/login")
def enroll(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.students.add(request.user)
    Notification.objects.create(
        user=course.teacher,
        message=f"{request.user.username} has enrolled in your course {course.title}",
    )
    return redirect("/dashboard")


@login_required(login_url="/login")
def unenroll(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.students.remove(request.user)
    Notification.objects.create(
        user=course.teacher,
        message=f"{request.user.username} has unenrolled from your course {course.title}",
    )
    return redirect("/dashboard")


# course = Course.objects.get(pk=course_id)
# course.students.add(request.user)

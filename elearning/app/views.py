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
    courses = Course.objects.all()
    return render(request, "home.html", {"courses": courses})


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
            {
                "courses": courses,
                "notifications": notifications,
            },
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


@login_required(login_url="/login")
def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    owns_course = course.teacher == request.user
    enrolled = course.students.filter(pk=request.user.pk).exists()
    students = course.students.all()
    return render(
        request,
        "dashboard/course/detail.html",
        {
            "course": course,
            "owns_course": owns_course,
            "enrolled": enrolled,
            "students": students,
        },
    )


# Helper for finding if the user is the owner of the course and a teacher
def owns_course(request, course_id):
    if not is_teacher(request.user):
        return False
    course = Course.objects.get(pk=course_id)
    return course.teacher == request.user


@login_required(login_url="/login")
@permission_required("app.change_course", login_url="/login", raise_exception=True)
def edit_course(request, course_id):
    # Verify that the user is a teacher and the owner of the course
    if not owns_course(request, course_id):
        return redirect("/dashboard")

    course = Course.objects.get(pk=course_id)

    # If the request is a POST request, process the form data and create a notification for each user
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            students = course.students.all()
            for student in students:
                Notification.objects.create(
                    user=student,
                    message=f"Your course '{course.title}' has been updated.",
                )
            return redirect("/dashboard")
    else:
        form = CourseForm(instance=course)
    return render(
        request, "dashboard/course/edit.html", {"form": form, "course": course}
    )


def remove_student(request, course_id, student_id):
    if not owns_course(request, course_id):
        return redirect("/dashboard")
    course = Course.objects.get(pk=course_id)
    student = User.objects.get(pk=student_id)
    course.students.remove(student)
    Notification.objects.create(
        user=student,
        message=f"You have been removed from the course {course.title}",
    )
    return redirect("/dashboard" + f"/courses/{course_id}")


# course = Course.objects.get(pk=course_id)
# course.students.add(request.user)

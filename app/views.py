# DJango auth imports
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.contrib.auth.models import Group, User

# Django page imports
from django.shortcuts import redirect, render

# Import forms
from .forms import CourseForm, FeedbackForm, RegisterForm, StatusForm

# Import models
from .models import Course, Feedback, Notification, Status

### HELPERS ###


# Helper for finding if the user is a teacher
def is_teacher(user):
    return user.groups.filter(name="teacher").exists()


# Helper for finding if the user is the owner of the course and a teacher
def owns_course(request, course_id):
    if not is_teacher(request.user):
        return False
    course = Course.objects.get(pk=course_id)
    return course.teacher == request.user


### VIEWS ###


# Home page
def home(request):
    courses = Course.objects.all()
    return render(request, "home.html", {"courses": courses})


# Logout user using auth logout then redirect to login page
def logoutUser(request):
    logout(request)
    return redirect("/login")


# Sign up user
def sign_up(request):
    # If the request is a POST request, process the form data
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add the user to the group they picked
            my_group = Group.objects.get(name=form.cleaned_data["group"])
            my_group.user_set.add(user)
            # Log the user in and redirect to the dashboard
            login(request, user)
            return redirect("/dashboard")
    else:
        form = RegisterForm()
    # Render the sign up page with the form
    return render(request, "registration/sign_up.html", {"form": form})


# Dashboard view (requires login)
@login_required(login_url="/login")
def dashboard(request):
    # Get the 5 most recent notifications and statuses
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-created_at"
    )[:5]
    statuses = Status.objects.all().order_by("-created_at")[:5]
    # If the user is a teacher, show the teacher dashboard
    if is_teacher(request.user):
        # Get teacher's courses
        courses = Course.objects.filter(teacher=request.user)
        return render(
            request,
            "dashboard/teacher.html",
            {
                "courses": courses,
                "notifications": notifications,
                "statuses": statuses,
            },
        )
    # If the user is a student, show the student dashboard
    else:
        # Get all courses that the student is not enrolled in
        recommended_courses = Course.objects.exclude(students=request.user)
        # Get all courses that the student is enrolled in
        enrolled_courses = Course.objects.filter(students=request.user)
        return render(
            request,
            "dashboard/student.html",
            {
                "recommended_courses": recommended_courses,
                "enrolled_courses": enrolled_courses,
                "notifications": notifications,
                "statuses": statuses,
            },
        )


# Search view (requires login)
@login_required(login_url="/login")
def search(request):
    # If the user is not a teacher, redirect to the dashboard
    if not is_teacher(request.user):
        return redirect("/dashboard")
    # Get the query from the request
    query = request.GET.get("query")
    users = []
    # If query, get all users that contain the query in their username
    if query:
        users = User.objects.filter(username__icontains=query)
    return render(request, "dashboard/search.html", {"query": query, "results": users})


# Create course view (requires login)
@login_required(login_url="/login")
def create_course(request):
    # If the user is not a teacher, redirect to the dashboard
    if not is_teacher(request.user):
        return redirect("/dashboard")

    # If it is a POST request, process the form data
    if request.method == "POST":
        # Get the form data with files
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the course and redirect to the dashboard
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect("/dashboard")
    else:
        form = CourseForm()
    # If the request is a GET, Render the create course page with the form
    return render(request, "dashboard/course/create.html", {"form": form})


# Enroll in a course (requires login)
@login_required(login_url="/login")
def enroll(request, course_id):
    # Get course and add req user to students
    course = Course.objects.get(pk=course_id)
    course.students.add(request.user)
    # Create a notification for the teacher that the user has enrolled
    Notification.objects.create(
        user=course.teacher,
        message=f"{request.user.username} has enrolled in your course {course.title}",
    )
    # Redirect to the dashboard (refreshes the page)
    return redirect("/dashboard")


# Unenroll from a course (requires login)
@login_required(login_url="/login")
def unenroll(request, course_id):
    # Get course and remove req user from students
    course = Course.objects.get(pk=course_id)
    course.students.remove(request.user)
    # Create a notification for the teacher that the user has unenrolled
    Notification.objects.create(
        user=course.teacher,
        message=f"{request.user.username} has unenrolled from your course {course.title}",
    )
    # Redirect to the dashboard (refreshes the page)
    return redirect("/dashboard")


# Course detail page (requires login)
@login_required(login_url="/login")
def course_detail(request, course_id):
    # Get course page data (course, owns_course *for conditionally rendering based on teacher, enrolled, students, feedback)
    course = Course.objects.get(pk=course_id)
    owns_course = course.teacher == request.user
    enrolled = course.students.filter(pk=request.user.pk).exists()
    students = course.students.all()
    feedback = Feedback.objects.filter(course=course)
    # Render the course detail page with the course data
    return render(
        request,
        "dashboard/course/detail.html",
        {
            "course": course,
            "owns_course": owns_course,
            "enrolled": enrolled,
            "students": students,
            "feedback": feedback,
        },
    )


# Edit course view (requires login and permission to change course)
@login_required(login_url="/login")
@permission_required("app.change_course", login_url="/login", raise_exception=True)
def edit_course(request, course_id):
    # Verify that the user is a teacher and the owner of the course
    if not owns_course(request, course_id):
        return redirect("/dashboard")

    course = Course.objects.get(pk=course_id)

    # If the request is a POST request, process the form data and create a notification for each user
    if request.method == "POST":
        # Get the form data with files and instance of the course
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            # Create a notification for each student in the course that it has been updated
            students = course.students.all()
            for student in students:
                Notification.objects.create(
                    user=student,
                    message=f"Your course '{course.title}' has been updated.",
                )
                # Redirect to the course detail page
            return redirect("/dashboard" + f"/courses/{course_id}")
    else:
        form = CourseForm(instance=course)
    # If the request is a GET, render the edit course page with the form and course data
    return render(
        request, "dashboard/course/edit.html", {"form": form, "course": course}
    )


# Remove student from course (requires login and permission to change course)
@login_required(login_url="/login")
@permission_required("app.change_course", login_url="/login", raise_exception=True)
def remove_student(request, course_id, student_id):
    # Verify that the user is a teacher and the owner of the course
    if not owns_course(request, course_id):
        return redirect("/dashboard")

    # Get course and studnet and remove student from course
    course = Course.objects.get(pk=course_id)
    student = User.objects.get(pk=student_id)
    course.students.remove(student)

    # Notify that student they have been removed
    Notification.objects.create(
        user=student,
        message=f"You have been removed from the course {course.title}",
    )

    # Redirect to the course detail page (refreshes the page)
    return redirect("/dashboard" + f"/courses/{course_id}")


# Create feedback view (requires login)
@login_required(login_url="/login")
def feedback(request, course_id):
    # If the request is a POST request, process the form data
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Save the feedback with the request user
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.course = Course.objects.get(pk=course_id)
            feedback.save()
            # Create a notification for the teacher that the user has left feedback
            Notification.objects.create(
                user=feedback.course.teacher,
                message=f"{request.user.username} has left feedback for your course {feedback.course.title}",
            )
            # Redirect to the course detail page (refreshes the page)
            return redirect("/dashboard" + f"/courses/{course_id}")


# Create status view (requires login)
@login_required(login_url="/login")
def status(request):
    # If the request is a POST request, process the form data
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            # Save the status with the request user
            status = form.save(commit=False)
            status.user = request.user
            status.save()
            # Redirect to the dashboard (refreshes the page)
            return redirect("/dashboard")

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/create-course/", views.create_course, name="create_course"),
    path("dashboard/search/", views.search, name="search"),
    path("logout/", views.logoutUser, name="logout"),
    path("courses/<int:course_id>/enroll", views.enroll, name="course_enroll"),
    path("courses/<int:course_id>/unenroll", views.unenroll, name="course_unenroll"),
    path(
        "dashboard/courses/<int:course_id>", views.course_detail, name="course_detail"
    ),
    path("courses/<int:course_id>/edit", views.edit_course, name="edit_course"),
    path(
        "courses/<int:course_id>/<int:student_id>/remove",
        views.remove_student,
        name="remove_student",
    ),
    path("courses/<int:course_id>/feedback", views.feedback, name="feedback"),
]

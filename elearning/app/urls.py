from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/create-course/", views.create_course, name="create_course"),
    path("logout/", views.logoutUser, name="logout"),
]

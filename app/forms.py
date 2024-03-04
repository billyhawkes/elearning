from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Course, Feedback, Status


# Register form with the additional fields
class RegisterForm(UserCreationForm):
    # Add the email, first_name, last_name
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    # Group allows you to choose between student and teacher
    group = forms.ChoiceField(
        choices=[("student", "Student"), ("teacher", "Teacher")], required=True
    )

    # Based on the model User
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


# Create course form with the title, description, and image
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "image"]


# Feedback creation form based on the Feedback model
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["feedback"]


# Status form based on the Status model
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["status"]

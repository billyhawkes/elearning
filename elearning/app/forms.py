from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Course, Feedback, Status


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    group = forms.ChoiceField(
        choices=[("student", "Student"), ("teacher", "Teacher")], required=True
    )

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


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]


class SearchForm(forms.Form):
    query = forms.CharField()


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["feedback"]


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["status"]

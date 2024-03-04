from django.contrib.auth.models import User
from django.db import models


# Course model with the title, description, teacher, students, image, and created_at fields
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name="students")
    # Image is stored as a url linking to the images/ route
    image = models.ImageField(null=True, upload_to="images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Notification model with the message, user, and created_at fields
class Notification(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# Status model with the status, user, and created_at fields
class Status(models.Model):
    status = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


# Feedback model with the feedback, user, created_at, and course fields
class Feedback(models.Model):
    feedback = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

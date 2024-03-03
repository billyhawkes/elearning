from django.contrib import admin

from .models import Course, Feedback, Notification, Status

# Register your models here.
admin.site.register(Course)
admin.site.register(Notification)
admin.site.register(Status)
admin.site.register(Feedback)

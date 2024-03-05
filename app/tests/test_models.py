from django.contrib.auth.models import User
from django.test import TestCase

from app.models import Course, Feedback, Notification, Status


# Test the models in the app
class ElearningModelTests(TestCase):
    # Set up by creating a teacher and a course
    def setUp(self):
        self.user = User.objects.create_user(
            {
                "username": "bilbobaggins123",
                "first_name": "Bilbo",
                "last_name": "Baggins",
                "email": "bilbo@gmail.com",
                "password1": "strongpassword1234",
                "password2": "strongpassword1234",
                "group": "teacher",
            }
        )
        self.course = Course.objects.create(
            title="The Ring 101",
            description="How to find the ring and not get killed by orcs.",
            teacher=self.user,
        )

    # Verify the course was created correctly
    def test_course_model(self):
        self.assertEqual(self.course.title, "The Ring 101")

    # Test notification creation
    def test_notification_model(self):
        notification = Notification.objects.create(
            message="Notification 1",
            user=self.user,
        )
        self.assertEqual(notification.message, "Notification 1")

    # Test status creation
    def test_status_model(self):
        status = Status.objects.create(
            status="Status 1",
            user=self.user,
        )
        self.assertEqual(status.status, "Status 1")

    # Test feedback creation
    def test_feedback_model(self):
        feedback = Feedback.objects.create(
            feedback="Feedback 1",
            user=self.user,
            course=self.course,
        )
        self.assertEqual(feedback.feedback, "Feedback 1")

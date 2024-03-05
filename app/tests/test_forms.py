from django.test import TestCase

from app.forms import CourseForm, FeedbackForm, RegisterForm, StatusForm


# Test all the forms in the app
class ELearningFormTests(TestCase):
    # Test register form correctly validates the data
    def test_register_form(self):
        form = RegisterForm(
            data={
                "username": "bilbobaggins123",
                "first_name": "Bilbo",
                "last_name": "Baggins",
                "email": "bilbo@gmail.com",
                "password1": "strongpassword1234",
                "password2": "strongpassword1234",
                "group": "student",
            }
        )
        self.assertTrue(form.is_valid())

    # Test course form correctly validates the data
    def test_course_form(self):
        form = CourseForm(
            data={
                "title": "The Ring 101",
                "description": "This is a test course",
                "image": "images/ring.jpg",
            }
        )
        self.assertTrue(form.is_valid())

    # Test feedback form correctly validates the data
    def test_feedback_form(self):
        form = FeedbackForm(data={"feedback": "great course!"})
        self.assertTrue(form.is_valid())

    # Test status form correctly validates the data
    def test_status_form(self):
        form = StatusForm(data={"status": "Ready for finals!"})
        self.assertTrue(form.is_valid())

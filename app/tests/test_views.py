# test_views.py
from django.contrib.auth.models import Group, User
from django.test import Client, TestCase

from app.models import Course


# Simple tests that verify each view is working correctly and returning the correct status / redirect
class ViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="bilbobaggins123", password="12345"
        )

        # Create a group
        self.group = Group.objects.create(name="teacher")
        self.group.user_set.add(self.user)

        # Create a course
        self.course = Course.objects.create(
            title="Test Course",
            teacher=self.user,
            description="This is a test course.",
            image="images/ring.jpg",
        )

        # Create client and login the user
        self.client = Client()
        logged_in = self.client.login(username="bilbobaggins123", password="12345")
        assert logged_in, "The test user could not log in."

    # Test the home view
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # Test logging out user
    def test_logoutUser(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)

    # Test sign up view
    def test_sign_up(self):
        response = self.client.get("/sign-up/")
        self.assertEqual(response.status_code, 200)

    # Test the dashboard
    def test_dashboard(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)

    # Test search view
    def test_search(self):
        response = self.client.get("/dashboard/search/")
        self.assertEqual(response.status_code, 200)

    # Test create course view
    def test_create_course(self):
        response = self.client.get("/dashboard/create-course/")
        self.assertEqual(response.status_code, 200)

    # Test enroll in course
    def test_enroll(self):
        response = self.client.get(f"/courses/{self.course.id}/enroll")
        self.assertEqual(response.status_code, 302)

    # Test unenroll in course
    def test_unenroll(self):
        response = self.client.get(f"/courses/{self.course.id}/unenroll")
        self.assertEqual(response.status_code, 302)

    # Test course detail view
    def test_course_detail(self):
        response = self.client.get(f"/dashboard/courses/{self.course.id}")
        self.assertEqual(response.status_code, 200)

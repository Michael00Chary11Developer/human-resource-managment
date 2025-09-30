from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAuthenticationIntegrationTest(APITestCase):
    """
    Integration tests for user authentication flow.
    """

    def setUp(self):
        """Set up test data."""
        self.registration_url = reverse("user-register")
        self.login_url = reverse("user-login")
        self.logout_url = reverse("user-logout")
        self.profile_url = reverse("user-profile")

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+1234567890",
            "department": "IT",
            "position": "Developer",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

    def test_complete_user_flow(self):
        """Test complete user registration, login, profile access, and logout flow."""

        # 1. Register a new user
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify user was created
        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

        # 2. Login with the new user
        login_data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Store tokens for later use
        access_token = response.data["tokens"]["access"]
        refresh_token = response.data["tokens"]["refresh"]

        print(f"refresh_token: {refresh_token}")

        # 3. Access profile with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

        # 4. Update profile
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone_number": "+9876543210",
            "department": "HR",
            "position": "Manager",
        }
        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")
        self.assertEqual(response.data["last_name"], "Name")

        # 5. Logout
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hr_manager_privileges(self):
        """Test HR manager privileges."""

        # Create a regular user
        regular_user = User.objects.create_user(
            username="regular", email="regular@example.com", password="testpass123"
        )

        # Create an HR manager
        hr_manager = User.objects.create_user(
            username="hrmanager",
            email="hr@example.com",
            password="testpass123",
            is_hr_manager=True,
        )

        # Test regular user can only see themselves
        self.client.force_authenticate(user=regular_user)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see at least themselves
        self.assertGreaterEqual(len(response.data), 1)

        # Test HR manager can see all users
        self.client.force_authenticate(user=hr_manager)
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see at least the 2 users we created
        self.assertGreaterEqual(len(response.data), 2)

    def test_password_change_flow(self):
        """Test password change flow."""

        # Create a user
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="oldpass123"
        )

        # Authenticate
        self.client.force_authenticate(user=user)

        # Change password
        change_password_data = {
            "old_password": "oldpass123",
            "new_password": "newpass123",
            "new_password_confirm": "newpass123",
        }

        response = self.client.patch(reverse("change-password"), change_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify password was changed
        user.refresh_from_db()
        self.assertTrue(user.check_password("newpass123"))
        self.assertFalse(user.check_password("oldpass123"))

    def test_authentication_required_endpoints(self):
        """Test that authentication is required for protected endpoints."""

        endpoints = [
            ("user-profile", "GET"),
            ("change-password", "PATCH"),
            ("user-list", "GET"),
            ("user-logout", "POST"),
        ]

        for endpoint, method in endpoints:
            url = reverse(endpoint)

            if method == "GET":
                response = self.client.get(url)
            elif method == "POST":
                response = self.client.post(url, {})
            elif method == "PATCH":
                response = self.client.patch(url, {})

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_registration(self):
        """Test that duplicate registration fails."""

        # Register first user
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to register with same email
        duplicate_data = self.user_data.copy()
        duplicate_data["username"] = "differentuser"

        response = self.client.post(self.registration_url, duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to register with same username
        duplicate_data = self.user_data.copy()
        duplicate_data["email"] = "different@example.com"

        response = self.client.post(self.registration_url, duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_login_attempts(self):
        """Test various invalid login attempts."""

        # Create a user
        User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Test with wrong password
        login_data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with wrong email
        login_data = {"email": "wrong@example.com", "password": "testpass123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with missing credentials
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

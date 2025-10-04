from django.contrib.auth import get_user_model
from django.test import TestCase

from users.serializers import (
    ChangePasswordSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class UserRegistrationSerializerTest(TestCase):
    """
    Test cases for UserRegistrationSerializer.
    """

    def setUp(self):
        """Set up test data."""
        self.valid_data = {
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

    def test_valid_registration_data(self):
        """Test valid registration data."""
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test password mismatch validation."""
        data = self.valid_data.copy()
        data["password_confirm"] = "differentpass"

        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_missing_required_fields(self):
        """Test missing required fields."""
        data = {"username": "testuser"}
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_create_user(self):
        """Test user creation through serializer."""
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))


class UserLoginSerializerTest(TestCase):
    """
    Test cases for UserLoginSerializer.
    """

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_valid_login_data(self):
        """Test valid login data."""
        data = {"email": "test@example.com", "password": "testpass123"}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_invalid_credentials(self):
        """Test invalid credentials."""
        data = {"email": "test@example.com", "password": "wrongpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_missing_credentials(self):
        """Test missing credentials."""
        data = {"email": "test@example.com"}
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class UserProfileSerializerTest(TestCase):
    """
    Test cases for UserProfileSerializer.
    """

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone_number="+1234567890",
            department="IT",
            position="Developer",
        )

    def test_serialize_user_profile(self):
        """Test serializing user profile."""
        serializer = UserProfileSerializer(self.user)
        data = serializer.data

        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["first_name"], "Test")
        self.assertEqual(data["last_name"], "User")
        self.assertEqual(data["phone_number"], "+1234567890")
        self.assertEqual(data["department"], "IT")
        self.assertEqual(data["position"], "Developer")
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)


class UserUpdateSerializerTest(TestCase):
    """
    Test cases for UserUpdateSerializer.
    """

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

    def test_update_user_profile(self):
        """Test updating user profile."""
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone_number": "+9876543210",
            "department": "HR",
            "position": "Manager",
        }

        serializer = UserUpdateSerializer(self.user, data=data)
        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "Name")
        self.assertEqual(updated_user.phone_number, "+9876543210")
        self.assertEqual(updated_user.department, "HR")
        self.assertEqual(updated_user.position, "Manager")


class ChangePasswordSerializerTest(TestCase):
    """
    Test cases for ChangePasswordSerializer.
    """

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="oldpass123"
        )

    def test_valid_password_change(self):
        """Test valid password change."""
        data = {
            "old_password": "oldpass123",
            "new_password": "newpass123",
            "new_password_confirm": "newpass123",
        }

        serializer = ChangePasswordSerializer(
            data=data,
            context={"request": type("obj", (object,), {"user": self.user})()},
        )
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test password mismatch in change password."""
        data = {
            "old_password": "oldpass123",
            "new_password": "newpass123",
            "new_password_confirm": "differentpass",
        }

        serializer = ChangePasswordSerializer(
            data=data,
            context={"request": type("obj", (object,), {"user": self.user})()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_wrong_old_password(self):
        """Test wrong old password."""
        data = {
            "old_password": "wrongpass",
            "new_password": "newpass123",
            "new_password_confirm": "newpass123",
        }

        serializer = ChangePasswordSerializer(
            data=data,
            context={"request": type("obj", (object,), {"user": self.user})()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("old_password", serializer.errors)

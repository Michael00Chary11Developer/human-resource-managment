from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    """
    Test cases for User model.
    """

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+1234567890",
            "department": "IT",
            "position": "Developer",
            "is_hr_manager": False,
        }

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.phone_number, "+1234567890")
        self.assertEqual(user.department, "IT")
        self.assertEqual(user.position, "Developer")
        self.assertFalse(user.is_hr_manager)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass123"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_user_str_representation(self):
        """Test string representation of user."""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.email} - {user.get_full_name()}"
        self.assertEqual(str(user), expected)

    def test_user_full_name(self):
        """Test user full name."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), "Test User")

    def test_user_short_name(self):
        """Test user short name."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_short_name(), "Test")

    def test_email_uniqueness(self):
        """Test email uniqueness constraint."""
        User.objects.create_user(**self.user_data)

        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            User.objects.create_user(
                username="testuser2",
                email="test@example.com",  # Same email
                password="testpass123",
            )

    def test_username_uniqueness(self):
        """Test username uniqueness constraint."""
        User.objects.create_user(**self.user_data)

        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            User.objects.create_user(
                username="testuser",  # Same username
                email="test2@example.com",
                password="testpass123",
            )

    def test_hr_manager_field(self):
        """Test HR manager field."""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_hr_manager)

        user.is_hr_manager = True
        user.save()
        self.assertTrue(user.is_hr_manager)

    def test_created_at_auto_now_add(self):
        """Test created_at field is automatically set."""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.created_at)

    def test_updated_at_auto_now(self):
        """Test updated_at field is automatically updated."""
        user = User.objects.create_user(**self.user_data)
        original_updated_at = user.updated_at

        user.first_name = "Updated"
        user.save()

        self.assertNotEqual(user.updated_at, original_updated_at)

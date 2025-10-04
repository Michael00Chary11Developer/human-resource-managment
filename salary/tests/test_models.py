from datetime import date
from decimal import Decimal

from django.test import TestCase

from personnel.models import Personnel
from salary.models import Salary
from users.models import User


class SalaryModelTest(TestCase):
    """
    Test cases for Salary model.
    """

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.personnel = Personnel.objects.create(
            user_id=self.user,
            number_of_personnel="EMP001",
            firstname="John",
            lastname="Doe",
            date_of_employment=date(2023, 1, 1),
            marital_status="married",
            have_child=True,
            number_of_child=2,
            religion="Islam",
            sort_of_religion="Sunni",
            birth_date=date(1990, 1, 1),
            degree="Bachelor",
            field_of_study="Computer Science",
            career_records="Software Developer",
            position="Developer",
            level_for_position="Senior",
        )

        self.salary_data = {
            "personnel": self.personnel,
            "user_id": self.user,
            "base_salary": Decimal("5000.00"),
            "housing_allowance": Decimal("1000.00"),
            "child_allowance": Decimal("500.00"),
            "groceries_allowance": Decimal("300.00"),
            "salary_start_date": date(2023, 1, 1),
        }

        # Don't create salary in setUp - let individual tests create their own

    def test_create_salary(self):
        """Test creating a salary record."""
        salary = Salary.objects.create(**self.salary_data)

        self.assertEqual(salary.personnel, self.personnel)
        self.assertEqual(salary.base_salary, Decimal("5000.00"))
        self.assertEqual(salary.housing_allowance, Decimal("1000.00"))
        self.assertEqual(salary.child_allowance, Decimal("500.00"))
        self.assertEqual(salary.groceries_allowance, Decimal("300.00"))
        self.assertEqual(salary.salary_start_date, date(2023, 1, 1))

    def test_salary_str_representation(self):
        """Test string representation of salary."""
        salary = Salary.objects.create(**self.salary_data)
        expected = f"{self.personnel.number_of_personnel} - {self.personnel.firstname}"
        self.assertEqual(str(salary), expected)

    def test_salary_one_to_one_relationship(self):
        """Test one-to-one relationship with personnel."""
        salary = Salary.objects.create(**self.salary_data)

        # Test that personnel has access to salary
        self.assertEqual(self.personnel.salaries, salary)

        # Test that salary has access to personnel
        self.assertEqual(salary.personnel, self.personnel)

    def test_salary_cascade_delete(self):
        """Test that salary is deleted when personnel is deleted."""
        salary = Salary.objects.create(**self.salary_data)
        salary_id = salary.personnel_id

        # Delete personnel
        self.personnel.delete()

        # Salary should be deleted too
        self.assertFalse(Salary.objects.filter(personnel_id=salary_id).exists())

    def test_salary_decimal_fields(self):
        """Test decimal field precision."""
        salary = Salary.objects.create(**self.salary_data)

        # Test that decimal values are stored correctly
        self.assertEqual(salary.base_salary, Decimal("5000.00"))
        self.assertEqual(salary.housing_allowance, Decimal("1000.00"))
        self.assertEqual(salary.child_allowance, Decimal("500.00"))
        self.assertEqual(salary.groceries_allowance, Decimal("300.00"))

    def test_salary_null_child_allowance(self):
        """Test that child_allowance can be null."""
        salary_data = self.salary_data.copy()
        salary_data["child_allowance"] = None

        salary = Salary.objects.create(**salary_data)
        self.assertIsNone(salary.child_allowance)

    def test_salary_date_fields(self):
        """Test date field handling."""
        salary = Salary.objects.create(**self.salary_data)

        self.assertEqual(salary.salary_start_date, date(2023, 1, 1))
        self.assertIsNotNone(salary.created_at)
        self.assertIsNotNone(salary.update_at)

    def test_salary_unique_personnel(self):
        """Test that each personnel can have only one salary record."""
        # Create first salary
        Salary.objects.create(**self.salary_data)

        # Try to create another salary for the same personnel
        with self.assertRaises(Exception):  # IntegrityError
            Salary.objects.create(**self.salary_data)

    def test_salary_with_different_personnel(self):
        """Test creating salary for different personnel."""
        # Create another personnel
        user2 = User.objects.create_user(
            username="testuser2", email="test2@example.com", password="testpass123"
        )

        personnel2 = Personnel.objects.create(
            user_id=user2,
            number_of_personnel="EMP002",
            firstname="Jane",
            lastname="Smith",
            date_of_employment=date(2023, 2, 1),
            marital_status="single",
            have_child=False,
            number_of_child=0,
            religion="Christian",
            sort_of_religion="Catholic",
            birth_date=date(1992, 5, 15),
            degree="Master",
            field_of_study="Business",
            career_records="Manager",
            position="Manager",
            level_for_position="Senior",
        )

        # Create salary for first personnel
        salary1 = Salary.objects.create(**self.salary_data)
        self.assertEqual(salary1.personnel, self.personnel)

        # Create salary for second personnel
        salary_data2 = self.salary_data.copy()
        salary_data2["personnel"] = personnel2
        salary_data2["user_id"] = user2

        salary2 = Salary.objects.create(**salary_data2)
        self.assertEqual(salary2.personnel, personnel2)

        # Both salaries should exist
        self.assertEqual(Salary.objects.count(), 2)

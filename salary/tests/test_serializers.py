from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from personnel.models import Personnel
from salary.models import Salary
from salary.serializer import PersonnelBasicSerializer, SalarySerializer
from users.models import User


class PersonnelBasicSerializerTest(TestCase):
    """
    Test cases for PersonnelBasicSerializer.
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

    def test_personnel_basic_serializer(self):
        """Test PersonnelBasicSerializer serialization."""
        serializer = PersonnelBasicSerializer(self.personnel)
        data = serializer.data

        self.assertEqual(data["number_of_personnel"], "EMP001")
        self.assertEqual(data["firstname"], "John")
        self.assertEqual(data["lastname"], "Doe")


class SalarySerializerTest(TestCase):
    """
    Test cases for SalarySerializer.
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
            "personnel": self.personnel.number_of_personnel,
            "base_salary": Decimal("5000.00"),
            "housing_allowance": Decimal("1000.00"),
            "child_allowance": Decimal("500.00"),
            "groceries_allowance": Decimal("300.00"),
            "salary_start_date": date(2023, 1, 1),
            "user_id": self.user.id,
        }

    def test_salary_serializer_creation(self):
        """Test creating salary through serializer."""
        serializer = SalarySerializer(data=self.salary_data)
        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())

        salary = serializer.save()
        self.assertEqual(salary.personnel, self.personnel)
        self.assertEqual(salary.base_salary, Decimal("5000.00"))
        self.assertEqual(salary.housing_allowance, Decimal("1000.00"))
        self.assertEqual(salary.child_allowance, Decimal("500.00"))
        self.assertEqual(salary.groceries_allowance, Decimal("300.00"))

    def test_salary_serializer_validation_single_no_children(self):
        """Test validation for single person with no children."""
        personnel = Personnel.objects.create(
            user_id=self.user,
            number_of_personnel="EMP002",
            firstname="Jane",
            lastname="Smith",
            date_of_employment=date(2023, 1, 1),
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

        data = self.salary_data.copy()
        data["personnel"] = personnel.number_of_personnel
        data["child_allowance"] = Decimal("500.00")

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_married_no_children(self):
        """Test validation for married person with no children."""
        personnel = Personnel.objects.create(
            user_id=self.user,
            number_of_personnel="EMP003",
            firstname="Bob",
            lastname="Johnson",
            date_of_employment=date(2023, 1, 1),
            marital_status="married",
            have_child=False,
            number_of_child=0,
            religion="Christian",
            sort_of_religion="Protestant",
            birth_date=date(1988, 3, 10),
            degree="Bachelor",
            field_of_study="Engineering",
            career_records="Engineer",
            position="Engineer",
            level_for_position="Senior",
        )

        data = self.salary_data.copy()
        data["personnel"] = personnel.number_of_personnel
        data["child_allowance"] = Decimal("500.00")

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_married_with_children_no_allowance(self):
        """Test validation for married person with children but no allowance."""
        data = self.salary_data.copy()
        data["child_allowance"] = None

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_child_allowance_exceeds_base_salary(self):
        """Test validation when child allowance exceeds base salary."""
        data = self.salary_data.copy()
        data["child_allowance"] = Decimal("6000.00")  # More than base salary

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_housing_allowance_exceeds_base_salary(self):
        """Test validation when housing allowance exceeds base salary."""
        data = self.salary_data.copy()
        data["housing_allowance"] = Decimal("6000.00")  # More than base salary

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_groceries_allowance_exceeds_housing(self):
        """Test validation when groceries allowance exceeds housing allowance."""
        data = self.salary_data.copy()
        data["groceries_allowance"] = Decimal("1500.00")  # More than housing allowance

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_salary_start_date_before_employment(self):
        """Test validation when salary start date is before employment date."""
        data = self.salary_data.copy()
        data["salary_start_date"] = date(2022, 12, 1)  # Before employment date

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_salary_start_date_future(self):
        """Test validation when salary start date is in the future."""
        data = self.salary_data.copy()
        data["salary_start_date"] = timezone.now().date() + timedelta(days=1)

        serializer = SalarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_validation_duplicate_personnel(self):
        """Test validation when personnel already has a salary record."""
        # Create first salary
        Salary.objects.create(
            personnel=self.personnel,
            user_id=self.user,
            base_salary=Decimal("5000.00"),
            housing_allowance=Decimal("1000.00"),
            child_allowance=Decimal("500.00"),
            groceries_allowance=Decimal("300.00"),
            salary_start_date=date(2023, 1, 1),
        )

        # Try to create another salary for the same personnel
        serializer = SalarySerializer(data=self.salary_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_salary_serializer_gross_salary_calculation(self):
        """Test gross salary calculation in serializer."""
        salary = Salary.objects.create(
            personnel=self.personnel,
            user_id=self.user,
            base_salary=Decimal("5000.00"),
            housing_allowance=Decimal("1000.00"),
            child_allowance=Decimal("500.00"),
            groceries_allowance=Decimal("300.00"),
            salary_start_date=date(2023, 1, 1),
        )

        serializer = SalarySerializer(salary)
        gross_salary = serializer.data["gross_salary"]

        # Expected: 5000 + 1000 + (2 * 500) + 300 = 7300
        expected = Decimal("7300.00")
        self.assertEqual(Decimal(str(gross_salary)), expected)

    def test_salary_serializer_net_salary_calculation(self):
        """Test net salary calculation in serializer."""
        salary = Salary.objects.create(
            personnel=self.personnel,
            user_id=self.user,
            base_salary=Decimal("5000.00"),
            housing_allowance=Decimal("1000.00"),
            child_allowance=Decimal("500.00"),
            groceries_allowance=Decimal("300.00"),
            salary_start_date=date(2023, 1, 1),
        )

        serializer = SalarySerializer(salary)
        net_salary = serializer.data["net_salary"]

        # Expected: 7300 * 0.9 = 6570
        expected = Decimal("6570.00")
        self.assertEqual(Decimal(str(net_salary)), expected)

    def test_salary_serializer_personnel_detail(self):
        """Test personnel detail in serializer."""
        salary = Salary.objects.create(
            personnel=self.personnel,
            user_id=self.user,
            base_salary=Decimal("5000.00"),
            housing_allowance=Decimal("1000.00"),
            child_allowance=Decimal("500.00"),
            groceries_allowance=Decimal("300.00"),
            salary_start_date=date(2023, 1, 1),
        )

        serializer = SalarySerializer(salary)
        personnel_detail = serializer.data["personnel_detail"]

        self.assertEqual(personnel_detail["number_of_personnel"], "EMP001")
        self.assertEqual(personnel_detail["firstname"], "John")
        self.assertEqual(personnel_detail["lastname"], "Doe")

    def test_salary_serializer_date_of_employment(self):
        """Test date of employment in serializer."""
        salary = Salary.objects.create(
            personnel=self.personnel,
            user_id=self.user,
            base_salary=Decimal("5000.00"),
            housing_allowance=Decimal("1000.00"),
            child_allowance=Decimal("500.00"),
            groceries_allowance=Decimal("300.00"),
            salary_start_date=date(2023, 1, 1),
        )

        serializer = SalarySerializer(salary)
        date_of_employment = serializer.data["date_of_employment"]

        self.assertEqual(date_of_employment, "2023-01-01")

    def test_salary_serializer_update(self):
        """Test updating salary through serializer."""
        salary = Salary.objects.create(
            personnel=self.personnel,
            user_id=self.user,
            base_salary=Decimal("5000.00"),
            housing_allowance=Decimal("1000.00"),
            child_allowance=Decimal("500.00"),
            groceries_allowance=Decimal("300.00"),
            salary_start_date=date(2023, 1, 1),
        )

        update_data = {
            "personnel": self.personnel.number_of_personnel,
            "base_salary": Decimal("6000.00"),
            "housing_allowance": Decimal("1200.00"),
            "child_allowance": Decimal("500.00"),
            "groceries_allowance": Decimal("300.00"),
            "salary_start_date": date(2023, 1, 1),
            "user_id": self.user.id,
        }

        serializer = SalarySerializer(salary, data=update_data, partial=True)
        if not serializer.is_valid():
            print(f"Update serializer errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())

        updated_salary = serializer.save()
        self.assertEqual(updated_salary.base_salary, Decimal("6000.00"))
        self.assertEqual(updated_salary.housing_allowance, Decimal("1200.00"))

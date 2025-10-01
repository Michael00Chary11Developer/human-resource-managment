from datetime import date, timedelta
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from personnel.models import Personnel
from salary.models import Salary
from users.models import User


class SalaryViewSetTest(APITestCase):
    """
    Test cases for SalaryViewSet.
    """

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Authenticate the user for all tests
        self.client.force_authenticate(user=self.user)

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

        self.salary = Salary.objects.create(
            personnel=self.personnel,
            user_id=self.user,
            base_salary=Decimal("5000.00"),
            housing_allowance=Decimal("1000.00"),
            child_allowance=Decimal("500.00"),
            groceries_allowance=Decimal("300.00"),
            salary_start_date=date(2023, 1, 1),
        )

        self.salary_data = {
            "personnel": self.personnel.number_of_personnel,
            "base_salary": "5000.00",
            "housing_allowance": "1000.00",
            "child_allowance": "500.00",
            "groceries_allowance": "300.00",
            "salary_start_date": "2023-06-01",
            "user_id": self.user.id,
        }

        self.client.force_authenticate(user=self.user)

    def test_list_salaries(self):
        """Test listing all salaries."""
        url = reverse("salary-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["base_salary"], "5000.00")

    def test_retrieve_salary(self):
        """Test retrieving a specific salary."""
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["base_salary"], "5000.00")
        self.assertEqual(response.data["housing_allowance"], "1000.00")
        self.assertEqual(response.data["child_allowance"], "500.00")
        self.assertEqual(response.data["groceries_allowance"], "300.00")

    def test_create_salary(self):
        """Test creating a new salary."""
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

        data = self.salary_data.copy()
        data["personnel"] = personnel2.number_of_personnel
        del data["child_allowance"]  # No children

        url = reverse("salary-list")
        response = self.client.post(url, data)

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["base_salary"], "5000.00")
        self.assertEqual(response.data["housing_allowance"], "1000.00")
        self.assertIsNone(response.data["child_allowance"])

    def test_create_salary_validation_errors(self):
        """Test salary creation with validation errors."""
        data = self.salary_data.copy()
        data["child_allowance"] = "6000.00"  # Exceeds base salary

        url = reverse("salary-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_update_salary(self):
        """Test updating a salary."""
        data = {
            "personnel": self.personnel.number_of_personnel,
            "base_salary": "6000.00",
            "housing_allowance": "1200.00",
            "child_allowance": "500.00",
            "groceries_allowance": "300.00",
            "salary_start_date": "2023-06-01",
            "user_id": self.user.id,
        }

        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.patch(url, data)

        if response.status_code != status.HTTP_200_OK:
            print(f"Update response status: {response.status_code}")
            print(f"Update response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["base_salary"], "6000.00")
        self.assertEqual(response.data["housing_allowance"], "1200.00")

    def test_delete_salary(self):
        """Test deleting a salary."""
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Salary.objects.filter(pk=self.salary.pk).exists())

    def test_salary_gross_salary_calculation(self):
        """Test gross salary calculation in API response."""
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("gross_salary", response.data)
        self.assertIn("net_salary", response.data)

        # Expected gross: 5000 + 1000 + (2 * 500) + 300 = 7300
        expected_gross = Decimal("7300.00")
        self.assertEqual(response.data["gross_salary"], expected_gross)

    def test_salary_net_salary_calculation(self):
        """Test net salary calculation in API response."""
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("net_salary", response.data)

        # Expected net: 7300 * 0.9 = 6570
        expected_net = Decimal("6570.00")
        self.assertEqual(response.data["net_salary"], expected_net)

    def test_salary_personnel_detail(self):
        """Test personnel detail in API response."""
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("personnel_detail", response.data)

        personnel_detail = response.data["personnel_detail"]
        self.assertEqual(personnel_detail["number_of_personnel"], "EMP001")
        self.assertEqual(personnel_detail["firstname"], "John")
        self.assertEqual(personnel_detail["lastname"], "Doe")

    def test_salary_date_of_employment(self):
        """Test date of employment in API response."""
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("date_of_employment", response.data)
        self.assertEqual(response.data["date_of_employment"], "2023-01-01")

    def test_salary_unauthorized_access(self):
        """Test unauthorized access to salary endpoints."""
        self.client.force_authenticate(user=None)

        # Test list
        url = reverse("salary-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test retrieve
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test create
        url = reverse("salary-list")
        response = self.client.post(url, self.salary_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test update
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.patch(url, {"base_salary": "6000.00"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test delete
        url = reverse("salary-detail", kwargs={"pk": self.salary.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_salary_duplicate_creation(self):
        """Test creating duplicate salary for same personnel."""
        data = self.salary_data.copy()

        url = reverse("salary-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_salary_future_start_date(self):
        """Test salary creation with future start date."""
        data = self.salary_data.copy()
        data["salary_start_date"] = (date.today() + timedelta(days=1)).strftime(
            "%Y-%m-%d"
        )

        url = reverse("salary-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_salary_start_date_before_employment(self):
        """Test salary creation with start date before employment."""
        data = self.salary_data.copy()
        data["salary_start_date"] = "2022-12-01"  # Before employment date

        url = reverse("salary-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_salary_housing_allowance_exceeds_base(self):
        """Test salary creation when housing allowance exceeds base salary."""
        data = self.salary_data.copy()
        data["housing_allowance"] = "6000.00"  # More than base salary

        url = reverse("salary-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_salary_groceries_allowance_exceeds_housing(self):
        """Test salary creation when groceries allowance exceeds housing allowance."""
        data = self.salary_data.copy()
        data["groceries_allowance"] = "1500.00"  # More than housing allowance

        url = reverse("salary-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

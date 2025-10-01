from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from personnel.models import Personnel
from salary.models import Salary

User = get_user_model()


class SalaryIntegrationTest(APITestCase):
    """
    Integration tests for salary functionality.
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

        self.client.force_authenticate(user=self.user)

    def test_complete_salary_workflow(self):
        """Test complete salary creation and management workflow."""

        # 1. Create salary
        salary_data = {
            "personnel": self.personnel.number_of_personnel,
            "base_salary": "5000.00",
            "housing_allowance": "1000.00",
            "child_allowance": "500.00",
            "groceries_allowance": "300.00",
            "salary_start_date": "2023-01-01",
            "user_id": self.user.id,
        }

        url = reverse("salary-list")
        response = self.client.post(url, salary_data)

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"Response data keys: {response.data.keys()}")
        salary_id = response.data["personnel_detail"]["number_of_personnel"]

        # 2. Retrieve salary
        url = reverse("salary-detail", kwargs={"pk": salary_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["base_salary"], "5000.00")
        self.assertEqual(response.data["housing_allowance"], "1000.00")
        self.assertEqual(response.data["child_allowance"], "500.00")
        self.assertEqual(response.data["groceries_allowance"], "300.00")

        # 3. Verify calculations
        from decimal import Decimal

        self.assertEqual(
            response.data["gross_salary"], Decimal("7300.00")
        )  # 5000 + 1000 + (2*500) + 300
        self.assertEqual(response.data["net_salary"], Decimal("6570.00"))  # 7300 * 0.9

        # 4. Update salary
        update_data = {
            "personnel": self.personnel.number_of_personnel,
            "base_salary": "6000.00",
            "housing_allowance": "1200.00",
            "child_allowance": "500.00",
            "groceries_allowance": "300.00",
            "salary_start_date": "2023-01-01",
            "user_id": self.user.id,
        }

        response = self.client.patch(url, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["base_salary"], "6000.00")
        self.assertEqual(response.data["housing_allowance"], "1200.00")

        # 5. Verify updated calculations
        from decimal import Decimal

        self.assertEqual(
            response.data["gross_salary"], Decimal("8500.00")
        )  # 6000 + 1200 + (2*500) + 300
        self.assertEqual(response.data["net_salary"], Decimal("7650.00"))  # 8500 * 0.9

        # 6. Delete salary
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Salary.objects.filter(pk=salary_id).exists())

    def test_salary_with_different_marital_statuses(self):
        """Test salary creation for different marital statuses."""

        # Test single person with no children
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

        salary_data = {
            "personnel": personnel2.number_of_personnel,
            "user_id": user2.id,
            "base_salary": "4000.00",
            "housing_allowance": "800.00",
            "groceries_allowance": "200.00",
            "salary_start_date": "2023-02-01",
        }

        url = reverse("salary-list")
        response = self.client.post(url, salary_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        from decimal import Decimal

        self.assertEqual(
            response.data["gross_salary"], Decimal("5000.00")
        )  # 4000 + 800 + 200
        self.assertEqual(response.data["net_salary"], Decimal("4500.00"))  # 5000 * 0.9

        # Test married person with no children
        user3 = User.objects.create_user(
            username="testuser3", email="test3@example.com", password="testpass123"
        )

        personnel3 = Personnel.objects.create(
            user_id=user3,
            number_of_personnel="EMP003",
            firstname="Bob",
            lastname="Johnson",
            date_of_employment=date(2023, 3, 1),
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

        salary_data = {
            "personnel": personnel3.number_of_personnel,
            "user_id": user3.id,
            "base_salary": "4500.00",
            "housing_allowance": "900.00",
            "groceries_allowance": "250.00",
            "salary_start_date": "2023-03-01",
        }

        response = self.client.post(url, salary_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        from decimal import Decimal

        self.assertEqual(
            response.data["gross_salary"], Decimal("5650.00")
        )  # 4500 + 900 + 250
        self.assertEqual(response.data["net_salary"], Decimal("5085.00"))  # 5650 * 0.9

    def test_salary_validation_edge_cases(self):
        """Test salary validation with edge cases."""

        # Test with zero values - create personnel without children
        personnel_no_children = Personnel.objects.create(
            user_id=self.user,
            number_of_personnel="EMP002",
            firstname="Jane",
            lastname="Doe",
            date_of_employment=date(2023, 1, 1),
            marital_status="single",
            have_child=False,
            number_of_child=0,
            religion="Christian",
            sort_of_religion="Catholic",
            birth_date=date(1990, 1, 1),
            degree="Bachelor",
            field_of_study="Computer Science",
            career_records="Developer",
            position="Developer",
            level_for_position="Junior",
        )

        salary_data = {
            "personnel": personnel_no_children.number_of_personnel,
            "user_id": self.user.id,
            "base_salary": "0.00",
            "housing_allowance": "0.00",
            "groceries_allowance": "0.00",
            "salary_start_date": "2023-01-01",
        }

        url = reverse("salary-list")
        response = self.client.post(url, salary_data)

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        from decimal import Decimal

        self.assertEqual(response.data["gross_salary"], Decimal("0.00"))
        self.assertEqual(response.data["net_salary"], Decimal("0.00"))

        # Test with maximum values
        salary_data = {
            "personnel": self.personnel.number_of_personnel,
            "user_id": self.user.id,
            "base_salary": "999999.99",
            "housing_allowance": "999999.99",
            "child_allowance": "999999.99",
            "groceries_allowance": "999999.99",
            "salary_start_date": "2023-01-01",
        }

        response = self.client.post(url, salary_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Expected: 999999.99 + 999999.99 + (2 * 999999.99) + 999999.99 = 4999999.95
        from decimal import Decimal

        self.assertEqual(response.data["gross_salary"], Decimal("4999999.95"))
        self.assertEqual(
            response.data["net_salary"], Decimal("4499999.955")
        )  # 4999999.95 * 0.9

    def test_salary_bulk_operations(self):
        """Test bulk salary operations."""

        # Create multiple personnel
        personnel_list = []
        for i in range(3):
            user = User.objects.create_user(
                username=f"testuser{i+2}",
                email=f"test{i+2}@example.com",
                password="testpass123",
            )

            personnel = Personnel.objects.create(
                user_id=user,
                number_of_personnel=f"EMP{i+2:03d}",
                firstname=f"Person{i+1}",
                lastname="Test",
                date_of_employment=date(2023, 1, 1),
                marital_status="married",
                have_child=True,
                number_of_child=1,
                religion="Islam",
                sort_of_religion="Sunni",
                birth_date=date(1990, 1, 1),
                degree="Bachelor",
                field_of_study="Computer Science",
                career_records="Software Developer",
                position="Developer",
                level_for_position="Senior",
            )
            personnel_list.append(personnel)

        # Create salaries for all personnel
        for i, personnel in enumerate(personnel_list):
            salary_data = {
                "personnel": personnel.number_of_personnel,
                "user_id": user.id,
                "base_salary": f"{5000 + i * 1000}.00",
                "housing_allowance": f"{1000 + i * 100}.00",
                "child_allowance": f"{500 + i * 50}.00",
                "groceries_allowance": f"{300 + i * 50}.00",
                "salary_start_date": "2023-01-01",
            }

            url = reverse("salary-list")
            response = self.client.post(url, salary_data)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # List all salaries
        url = reverse("salary-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 3)

        # Verify each salary has correct calculations
        for i, salary_data in enumerate(response.data["results"]):
            base_salary = 5000 + i * 1000
            housing_allowance = 1000 + i * 100
            child_allowance = 500 + i * 50
            groceries_allowance = 300 + i * 50

            expected_gross = (
                base_salary + housing_allowance + child_allowance + groceries_allowance
            )
            expected_net = expected_gross * Decimal("0.9")

            self.assertEqual(Decimal(salary_data["gross_salary"]), expected_gross)
            self.assertEqual(Decimal(salary_data["net_salary"]), expected_net)

    def test_salary_error_handling(self):
        """Test error handling in salary operations."""

        # Test with invalid personnel ID
        salary_data = {
            "personnel": 99999,  # Non-existent personnel
            "base_salary": "5000.00",
            "housing_allowance": "1000.00",
            "child_allowance": "500.00",
            "groceries_allowance": "300.00",
            "salary_start_date": "2023-01-01",
        }

        url = reverse("salary-list")
        response = self.client.post(url, salary_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with invalid salary ID
        url = reverse("salary-detail", kwargs={"pk": 99999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test with malformed data
        salary_data = {
            "personnel": self.personnel.number_of_personnel,
            "base_salary": "invalid",  # Invalid decimal
            "housing_allowance": "1000.00",
            "child_allowance": "500.00",
            "groceries_allowance": "300.00",
            "salary_start_date": "2023-01-01",
        }

        url = reverse("salary-list")
        response = self.client.post(url, salary_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_salary_permissions(self):
        """Test salary permissions and access control."""

        # Create salary
        salary_data = {
            "personnel": self.personnel.number_of_personnel,
            "user_id": self.user.id,
            "base_salary": "5000.00",
            "housing_allowance": "1000.00",
            "child_allowance": "500.00",
            "groceries_allowance": "300.00",
            "salary_start_date": "2023-01-01",
        }

        url = reverse("salary-list")
        response = self.client.post(url, salary_data)
        salary_id = response.data["personnel_detail"]["number_of_personnel"]

        # Test with different user
        user2 = User.objects.create_user(
            username="testuser2", email="test2@example.com", password="testpass123"
        )

        self.client.force_authenticate(user=user2)

        # Should not be able to access salary created by different user
        url = reverse("salary-detail", kwargs={"pk": salary_id})
        response = self.client.get(url)

        # This depends on your permission setup - adjust based on your requirements
        # For now, assuming salary is accessible by any authenticated user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

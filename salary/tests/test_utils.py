from decimal import Decimal

from django.test import TestCase

from salary.utils import calculate_gross_salary, calculate_net_salary


class SalaryUtilsTest(TestCase):
    """
    Test cases for salary utility functions.
    """

    def test_calculate_gross_salary_single_person(self):
        """Test gross salary calculation for single person."""
        base_salary = Decimal("5000.00")
        housing_allowance = Decimal("1000.00")
        child_allowance = Decimal("500.00")
        food_allowance = Decimal("300.00")
        number_of_child = 0
        marital_status = "single"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        expected = base_salary + housing_allowance + food_allowance
        self.assertEqual(result, expected)

    def test_calculate_gross_salary_married_no_children(self):
        """Test gross salary calculation for married person with no children."""
        base_salary = Decimal("5000.00")
        housing_allowance = Decimal("1000.00")
        child_allowance = Decimal("500.00")
        food_allowance = Decimal("300.00")
        number_of_child = 0
        marital_status = "married"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        expected = base_salary + housing_allowance + food_allowance
        self.assertEqual(result, expected)

    def test_calculate_gross_salary_married_with_children(self):
        """Test gross salary calculation for married person with children."""
        base_salary = Decimal("5000.00")
        housing_allowance = Decimal("1000.00")
        child_allowance = Decimal("500.00")
        food_allowance = Decimal("300.00")
        number_of_child = 2
        marital_status = "married"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        expected = (
            base_salary
            + housing_allowance
            + (number_of_child * child_allowance)
            + food_allowance
        )
        self.assertEqual(result, expected)

    def test_calculate_gross_salary_married_with_children_none_allowance(self):
        """Test gross salary calculation when child_allowance is None."""
        base_salary = Decimal("5000.00")
        housing_allowance = Decimal("1000.00")
        child_allowance = None
        food_allowance = Decimal("300.00")
        number_of_child = 2
        marital_status = "married"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        expected = (
            base_salary
            + housing_allowance
            + (number_of_child * Decimal("0"))
            + food_allowance
        )
        self.assertEqual(result, expected)

    def test_calculate_gross_salary_married_with_children_zero_allowance(self):
        """Test gross salary calculation when child_allowance is 0."""
        base_salary = Decimal("5000.00")
        housing_allowance = Decimal("1000.00")
        child_allowance = Decimal("0.00")
        food_allowance = Decimal("300.00")
        number_of_child = 2
        marital_status = "married"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        expected = (
            base_salary
            + housing_allowance
            + (number_of_child * child_allowance)
            + food_allowance
        )
        self.assertEqual(result, expected)

    def test_calculate_gross_salary_married_with_children_none_number(self):
        """Test gross salary calculation when number_of_child is None."""
        base_salary = Decimal("5000.00")
        housing_allowance = Decimal("1000.00")
        child_allowance = Decimal("500.00")
        food_allowance = Decimal("300.00")
        number_of_child = None
        marital_status = "married"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        expected = base_salary + housing_allowance + food_allowance
        self.assertEqual(result, expected)

    def test_calculate_net_salary_default_tax_rate(self):
        """Test net salary calculation with default tax rate (10%)."""
        gross_salary = Decimal("10000.00")

        result = calculate_net_salary(gross_salary)

        expected = gross_salary * (Decimal("1") - Decimal("0.1"))
        self.assertEqual(result, expected)
        self.assertEqual(result, Decimal("9000.00"))

    def test_calculate_net_salary_custom_tax_rate(self):
        """Test net salary calculation with custom tax rate."""
        gross_salary = Decimal("10000.00")
        tax_rate = Decimal("0.15")

        result = calculate_net_salary(gross_salary, tax_rate)

        expected = gross_salary * (Decimal("1") - tax_rate)
        self.assertEqual(result, expected)
        self.assertEqual(result, Decimal("8500.00"))

    def test_calculate_net_salary_zero_tax_rate(self):
        """Test net salary calculation with zero tax rate."""
        gross_salary = Decimal("10000.00")
        tax_rate = Decimal("0.00")

        result = calculate_net_salary(gross_salary, tax_rate)

        expected = gross_salary * (Decimal("1") - tax_rate)
        self.assertEqual(result, expected)
        self.assertEqual(result, gross_salary)

    def test_calculate_net_salary_high_tax_rate(self):
        """Test net salary calculation with high tax rate."""
        gross_salary = Decimal("10000.00")
        tax_rate = Decimal("0.50")

        result = calculate_net_salary(gross_salary, tax_rate)

        expected = gross_salary * (Decimal("1") - tax_rate)
        self.assertEqual(result, expected)
        self.assertEqual(result, Decimal("5000.00"))

    def test_calculate_gross_salary_edge_cases(self):
        """Test gross salary calculation with edge cases."""
        base_salary = Decimal("0.00")
        housing_allowance = Decimal("0.00")
        child_allowance = Decimal("0.00")
        food_allowance = Decimal("0.00")
        number_of_child = 0
        marital_status = "single"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        self.assertEqual(result, Decimal("0.00"))

    def test_calculate_gross_salary_large_numbers(self):
        """Test gross salary calculation with large numbers."""
        base_salary = Decimal("999999.99")
        housing_allowance = Decimal("999999.99")
        child_allowance = Decimal("999999.99")
        food_allowance = Decimal("999999.99")
        number_of_child = 10
        marital_status = "married"

        result = calculate_gross_salary(
            base_salary,
            housing_allowance,
            child_allowance,
            food_allowance,
            number_of_child,
            marital_status,
        )

        expected = (
            base_salary
            + housing_allowance
            + (number_of_child * child_allowance)
            + food_allowance
        )
        self.assertEqual(result, expected)

from django.db import models

from core.models import BaseModelDate
from personnel.models import Personnel


class Salary(BaseModelDate):
    """
    Model representing the salary details for personnel.

    This model inherits from BaseModelDate to include created and updated timestamps.
    It establishes a one-to-one relationship with the Personnel model,
    ensuring that each personnel has a unique salary record.

    Attributes:
        personnel (OneToOneField): The personnel associated with this salary record.
        base_salary (DecimalField): The base salary of the personnel.
        housing_allowance (DecimalField): The housing allowance for the personnel.
        child_allowance (DecimalField, optional): The child allowance for the personnel, if applicable.
        food_allowance (DecimalField): The food allowance for the personnel.
        salary_start_date (DateField): The date when the salary starts.

    Methods:
        __str__(): Returns a string representation of the Salary instance,
                    displaying the personnel's number and first name.
    """

    personnel = models.OneToOneField(
        Personnel, on_delete=models.CASCADE, related_name="salaries", primary_key=True
    )

    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    housing_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    child_allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    groceries_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    salary_start_date = models.DateField()

    def __str__(self):
        return f"{self.personnel.number_of_personnel} - {self.personnel.firstname}"

import random

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModelDate


class Personnel(BaseModelDate):
    """
    Inherits from BaseModelDate to include created and updated timestamps.
    Model representing personnel information, including personal details,
    education, career records, and employment data. Each personnel has a
    unique identifier in the format '100XXX'. The model contains fields for
    first name, last name, marital status, children information, religion,
    phone number, birth date, education, career history, position, level,
    and date of employment. The unique personnel number is generated
    automatically upon creation.
    """

    def create_new_number_of_personnel():
        """Generates a unique personnel number in the format '100XXX'."""
        try:
            while True:
                random_number = random.randint(1, 999)
                costum_format = f"100{random_number:03d}"

                if not Personnel.objects.filter(
                    number_of_personnel=costum_format
                ).exists():

                    return costum_format
        except Exception:
            raise Exception(
                "Sorry",
                "All number has been generate!! for solution call to programmer!",
            )

    number_of_personnel = models.CharField(
        max_length=6,
        blank=True,
        editable=False,
        unique=True,
        default=create_new_number_of_personnel,
        primary_key=True,
    )

    # Personnel information
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=10)
    have_child = models.BooleanField()
    number_of_child = models.PositiveSmallIntegerField(null=True, blank=True)
    religion = models.CharField(max_length=20)
    sort_of_religion = models.CharField(max_length=20)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    birth_date = models.DateField()

    # Educational records
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)

    # Career records
    career_records = models.TextField()

    # Position and level
    position = models.CharField(max_length=100)
    level_for_position = models.CharField(max_length=100)

    # Date when the personnel was employed.
    date_of_employment = models.DateField()

    def __str__(self):
        """String representation of the Personnel model."""

        return f"{self.number_of_personnel} - {self.firstname} - {self.lastname}"

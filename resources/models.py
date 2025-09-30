from django.db import models

from core.models import BaseModelDate
from personnel.models import Personnel

from .utils import CreateUniqueCode

"""
Represents a resource in the system with various attributes.
Attributes:
    asset_code (str): A unique identifier for the resource. This field is set automatically
                      if not provided, using a method from CreateUniqueCode.
    resource_sort (str): The category or type of the resource. This field is optional.
    date_of_allocation (date): The date when the resource was allocated. This field is required.

Methods:
    save(*args, **kwargs):
        Overrides the default save method to set a unique asset_code if not provided.

"""


class Resources(BaseModelDate):

    number_of_personnel = models.OneToOneField(
        Personnel,
        related_name="number_of_personnel_ex",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    asset_code = models.CharField(max_length=8, editable=False, blank=False)
    resource_name = models.CharField(
        max_length=20, blank=False, unique=False, editable=True
    )
    resource_sort = models.CharField(max_length=20, blank=False, editable=True)
    dateـofـallocation = models.DateField()

    def __str__(self) -> str:
        return f"{self.resource_name}\t{self.resource_sort}\t{self.dateـofـallocation}"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to generate a unique asset_code
        if it is not provided during resource creation.
        """
        if not self.asset_code:
            self.asset_code = CreateUniqueCode.generate_unique_code(Resources)
        super().save(*args, **kwargs)

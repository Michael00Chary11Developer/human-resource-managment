from django.utils import timezone
from rest_framework import serializers

from core.serializer import BaseCoreSerializer
from personnel.models import Personnel

from .models import Resources

"""
serializr class that serialize mean convert json to python object python object to json
    Attributes:
        get all attribute of Resourcse in fields for serialize:
                -asset_code (str): A unique identifier for the resource. This field is set automatically
                          if not provided, using a method from CreateUniqueCode.
                          CreateUniqueCode is in utils.py
                -resource_sort (str): The category or type of the resource. This field is optional.
                -date_of_allocation (date): The date when the resource was allocated. This field is required.
    models:
        Resource and say which model must be serialize
"""


class PersonnelDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Personnel details.

    Attributes:
        number_of_personnel (int): The unique identifier for the personnel.
        firstname (str): The first name of the personnel.
        lastname (str): The last name of the personnel.
    """

    class Meta:
        model = Personnel
        fields = ["number_of_personnel", "firstname", "lastname"]


class ResourceSerializer(BaseCoreSerializer):
    """
    Serializer for Resources model.

    Attributes:
        user (int): The ID of the user associated with the resource (read-only).
        number_of_personnel (int): The unique identifier for the personnel associated with the resource (write-only).
        personnel_detail (PersonnelDetailSerializer): Nested serializer for personnel details (read-only).
    """

    date_of_employment = serializers.DateField(
        source="number_of_personnel.date_of_employment", read_only=True
    )

    number_of_personnel = serializers.PrimaryKeyRelatedField(
        queryset=Personnel.objects.all(), write_only=True
    )

    personnel_detail = PersonnelDetailSerializer(
        source="number_of_personnel", read_only=True
    )

    class Meta:
        model = Resources
        fields = (
            [BaseCoreSerializer.Meta.fields[0]]
            + [
                "number_of_personnel",
                "personnel_detail",
                "asset_code",
                "resource_name",
                "resource_sort",
                "date_of_employment",
                "dateـofـallocation",
            ]
            + [BaseCoreSerializer.Meta.fields[1]]
            + [BaseCoreSerializer.Meta.fields[2]]
        )
        read_only_fields = BaseCoreSerializer.Meta.read_only_fields

    def validate(self, data):
        """
        Custom validation for resource allocation data.

        Checks that the date of allocation is not ahead of the personnel's date of employment
        and that it is not set in the future.


        """

        date_time_allocation = data.get("dateـofـallocation")
        number_of_personnel: Personnel = data.get("number_of_personnel")
        date_of_employment = number_of_personnel.date_of_employment
        today = timezone.now().date()

        # Validate date of allocation
        if date_of_employment > date_time_allocation:
            raise serializers.ValidationError(
                "The date of allocation cannot being ahead of date_of_employment"
            )
        if date_time_allocation > today:
            raise serializers.ValidationError(
                "The date of allocation cannot being ahead of today!"
            )

        if self.instance:
            if self.instance.number_of_personnel == number_of_personnel:
                return data

        if Resources.objects.filter(number_of_personnel=number_of_personnel).exists():
            raise serializers.ValidationError(
                f"A resource record for personnel {number_of_personnel} already exists."
            )

        return data

from decimal import Decimal

from rest_framework import serializers

from personnel.models import Personnel
from resources.models import Resources
from salary.models import Salary
from salary.utils import calculate_gross_salary, calculate_net_salary

from .models import BaseModelDate


class BaseCoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the base model that includes creation and update timestamps.
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    update_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = BaseModelDate
        fields = ["user_id", "created_at", "update_at"]
        read_only_fields = ["user_id"]


class ResourcesDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Salary model that includes salary details and computed fields for gross and net salary.
    """

    class Meta:
        model = Resources
        fields = ["asset_code", "resource_name", "resource_sort", "dateـofـallocation"]


class SalaryDetailSerializer(serializers.ModelSerializer):

    gross_salary = serializers.SerializerMethodField(read_only=True)

    """
    Computed gross salary for the personnel. This field is read-only.
    """
    net_salary = serializers.SerializerMethodField(read_only=True)

    """
    Computed net salary for the personnel after tax deductions. This field is read-only.
    """

    class Meta:
        model = Salary
        fields = [
            "salary_start_date",
            "gross_salary",
            "net_salary",
        ]

    def get_gross_salary(self, obj: Salary) -> Decimal:
        """
        Calculate and return the gross salary for the personnel.

        The gross salary is calculated based on the base salary, housing allowance,
        child allowance, food allowance, number of children, and marital status of the personnel.
        """
        return calculate_gross_salary(
            obj.base_salary,
            obj.housing_allowance,
            obj.child_allowance,
            obj.groceries_allowance,
            obj.personnel.number_of_child,
            obj.personnel.marital_status.lower(),
        )

    def get_net_salary(self, obj: Salary) -> Decimal:
        """
        Calculate and return the net salary for the personnel.

        The net salary is computed by deducting tax from the gross salary.
        """
        gross = self.get_gross_salary(obj)
        return calculate_net_salary(gross)


class PersonnelGetAllDataSerializer(serializers.ModelSerializer):
    """
    Serializer for Personnel model that includes personal information,
    as well as nested salary and resource details.
    """

    salary_detail = serializers.SerializerMethodField()
    resource_detail = serializers.SerializerMethodField()

    class Meta:
        model = Personnel
        fields = (
            [BaseCoreSerializer.Meta.fields[0]]
            + [
                "number_of_personnel",
                "firstname",
                "lastname",
                "position",
                "resource_detail",
                "salary_detail",
                "date_of_employment",
                "level_for_position",
            ]
            + [BaseCoreSerializer.Meta.fields[1]]
            + [BaseCoreSerializer.Meta.fields[2]]
        )

    def get_salary_detail(self, obj: Personnel) -> dict | None:
        """
        Retrieve and serialize salary details for the personnel.

        Args:
            obj (Personnel): The Personnel instance for which to get salary details.

        Returns:
            dict or None: Serialized salary details or None if no salary is found.
        """

        salary = Salary.objects.filter(personnel=obj.number_of_personnel).first()
        if salary:
            return SalaryDetailSerializer(salary).data
        return None

    def get_resource_detail(self, obj: Personnel) -> dict | None:
        """
        Retrieve and serialize resource details for the personnel.

        Args:
            obj (Personnel): The Personnel instance for which to get resource details.

        Returns:
            dict or None: Serialized resource details or None if no resource is found.
        """

        resource = Resources.objects.filter(
            number_of_personnel=obj.number_of_personnel
        ).first()
        if resource:
            return ResourcesDetailSerializer(resource).data
        return None

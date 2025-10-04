from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from core.serializer import BaseCoreSerializer
from core.utils import CleanData
from personnel.models import Personnel
from users.models import User

from .models import Salary
from .utils import calculate_gross_salary, calculate_net_salary


class PersonnelBasicSerializer(serializers.ModelSerializer):
    """
    Basic serializer for the Personnel model.

    This serializer converts the Personnel model fields into JSON format.
    """

    class Meta:
        model = Personnel
        fields = ["number_of_personnel", "firstname", "lastname"]


class SalarySerializer(BaseCoreSerializer):
    """
    Serializer for the Salary model.

    This serializer handles the serialization and validation of salary data
    for personnel, including the calculation of gross and net salaries.
    """

    personnel = serializers.PrimaryKeyRelatedField(
        queryset=Personnel.objects.all(), write_only=True
    )

    """
    The personnel associated with the salary. This field is write-only.
    """
    personnel_detail = PersonnelBasicSerializer(source="personnel", read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    """
    Detailed information about the personnel. This field is read-only.
    """

    gross_salary = serializers.SerializerMethodField(read_only=True)

    """
    Computed gross salary for the personnel. This field is read-only.
    """
    net_salary = serializers.SerializerMethodField(read_only=True)

    """
    Computed net salary for the personnel after tax deductions. This field is read-only.
    """

    date_of_employment = serializers.DateField(
        source="personnel.date_of_employment", read_only=True
    )

    class Meta:

        model = Salary
        fields = [
            "user_id",
            "personnel",
            "personnel_detail",
            "base_salary",
            "housing_allowance",
            "child_allowance",
            "groceries_allowance",
            "date_of_employment",
            "salary_start_date",
            "gross_salary",
            "net_salary",
            "created_at",
            "update_at",
        ]

        read_only_fields = BaseCoreSerializer.Meta.read_only_fields

        """
        List of fields that cannot be modified during serialization.
        """

    def get_gross_salary(self, obj: Salary) -> Decimal:
        """
        Calculate and return the gross salary for the personnel.

        The gross salary is calculated based on the base salary, housing allowance,
        child allowance, groceries allowance, number of children, and marital status of the personnel.
        """
        return calculate_gross_salary(
            obj.base_salary,
            obj.housing_allowance,
            obj.child_allowance,
            obj.groceries_allowance,
            obj.personnel.number_of_child,
            CleanData(obj.personnel.marital_status).created_clean(),
        )

    def get_net_salary(self, obj: Salary) -> Decimal:
        """
        Calculate and return the net salary for the personnel.

        The net salary is computed by deducting tax from the gross salary.
        """
        gross = self.get_gross_salary(obj)
        return calculate_net_salary(gross)

    def validate(self, data):
        """
        Validate the salary data before saving.

        This method checks whether the personnel is eligible for child allowance
        based on their marital status and number of children. It also ensures that
        there is no existing salary record for the same personnel.
        """
        personnel: Personnel = data.get("personnel")
        child_allowance = data.get("child_allowance")
        salary_start_date = data.get("salary_start_date")
        base_salary = data.get("base_salary")
        housing_allowance = data.get("housing_allowance")
        groceries_allowance = data.get("groceries_allowance")

        if (
            personnel.marital_status != "married"
            or personnel.marital_status == "married"
            and personnel.number_of_child in [0, None]
        ):
            if child_allowance not in [0, None]:
                raise serializers.ValidationError(
                    "Personnel with no children or single or another marital except married cannot have a child allowance."
                )
        elif (
            personnel.marital_status == "married"
            and personnel.number_of_child not in [0, None]
        ):
            if child_allowance is None or child_allowance == 0:
                raise serializers.ValidationError(
                    "The Person Who have child must have child_allowance"
                )

        if child_allowance is not None and child_allowance > base_salary:
            raise serializers.ValidationError(
                "child_allowance cannot be more base_salary"
            )

        if housing_allowance > base_salary:
            raise serializers.ValidationError(
                "housing_allowance cannot be more base_salary"
            )

        if groceries_allowance > housing_allowance:
            raise serializers.ValidationError(
                "groceries_allowance cannot be more housing_allowance"
            )

        if salary_start_date < personnel.date_of_employment:
            raise serializers.ValidationError(
                "The date_of_employment cannot being ahead of salary_start_date"
            )

        if salary_start_date > timezone.now().date():
            raise serializers.ValidationError(
                "The salary_start_date cannot be in the future."
            )

        if self.instance:
            if self.instance.personnel == personnel:
                return data

        if Salary.objects.filter(personnel=personnel).exists():
            raise serializers.ValidationError(
                f"A salary record for personnel {personnel} already exists."
            )

        return data

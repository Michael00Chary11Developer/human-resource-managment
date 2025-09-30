from django.utils import timezone
from rest_framework import serializers

from core.serializer import BaseCoreSerializer
from core.utils import CleanData

from .models import Personnel


class PersonnelSerializer(BaseCoreSerializer):
    """
    Serializer for the Personnel model.

    This serializer handles the conversion between Personnel model instances
    and JSON representations, allowing for easy input and output of personnel
    data through API endpoints.
    """

    class Meta:
        model = Personnel
        fields = (
            [BaseCoreSerializer.Meta.fields[0]]
            + [
                "number_of_personnel",
                "firstname",
                "lastname",
                "marital_status",
                "have_child",
                "number_of_child",
                "religion",
                "sort_of_religion",
                "phone_number",
                "birth_date",
                "degree",
                "field_of_study",
                "career_records",
                "position",
                "level_for_position",
                "date_of_employment",
            ]
            + [BaseCoreSerializer.Meta.fields[1]]
            + [BaseCoreSerializer.Meta.fields[2]]
        )
        read_only_fields = BaseCoreSerializer.Meta.read_only_fields
        """
        Include all fields from the Personnel model in the serialized output.
        """

    def validate(self, data):
        """
        Validate the input data for the PersonnelSerializer.

        This method checks the following conditions:
        1. Ensures that the 'birth_date' is not in the future.
        2. Ensures that the 'date_of_employment' is not before the 'birth_date'.
        3. Ensures that the 'date_of_employment' is not in the future.
        4. Validates marital status and children information.

        Args:
            data (dict): The input data containing the fields to be validated.

        Raises:
            serializers.ValidationError: If any of the validation checks fail.

        Returns:
            dict: The validated data if no errors are raised.
        """

        birth_date = data.get("birth_date")
        date_of_employment = data.get("date_of_employment")
        today = timezone.now().date()

        marital_status = CleanData(data.get("marital_status")).created_clean()
        data["marital_status"] = marital_status
        have_child = data.get("have_child")
        number_of_child = data.get("number_of_child")

        if marital_status != "married":
            if have_child is not False or number_of_child not in [None, 0]:
                raise serializers.ValidationError(
                    "Unmarried person cannot have children!"
                )

        else:
            if have_child is False and number_of_child not in [None, 0]:
                raise serializers.ValidationError(
                    "If no child, 'number_of_child' must be blank."
                )
            elif have_child is True and number_of_child in [0, None]:
                raise serializers.ValidationError(
                    "you must have enter number of child!"
                )

        if birth_date > today:
            raise serializers.ValidationError("Birth date cannot be in the future.")

        if date_of_employment < birth_date:
            raise serializers.ValidationError(
                "Date of employment cannot be before birth date."
            )

        if date_of_employment > today:
            raise serializers.ValidationError(
                "Date of employment cannot be in the future."
            )

        return data

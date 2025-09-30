from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from core.serializer import BaseCoreSerializer

from .models import Recruitment

"""
Serializer for the Recruitment model.

This serializer handles the serialization and validation of
Recruitment instances.

Attributes:
    time_spent (timedelta): A calculated field that represents the
                            total time spent on interviews.
                            calculate by method in model->interview_spent_time_calculate
"""


class RecruitmentSerializer(BaseCoreSerializer):
    """
    Serializer class for the Recruitment model.

    This class serializes all fields of the Recruitment model except
    for the 'recruiment_id' field

    Attributes:
        user_id=readonly is primarykey of models of core and set on model recruiment
        time_spent (SerializerMethodField): Calculates and returns
                                            the total time spent on
                                            interviews.
    """

    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    time_spent = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for configuring the Recruitment serializer.

        Attributes:
            model (Model): Specifies the model to be serialized.
            fields (list): List of model fields to be included in the serialization.
        """

        model = Recruitment
        fields = (
            [BaseCoreSerializer.Meta.fields[0]]
            + [
                "recruitment_id",
                "received_resume",
                "checked_resume",
                "approved_resume",
                "interviewed_resume",
                "duration_every_interview",
                "time_spent",
                "recruitment_position",
                "recruitment_level_position",
                "recruitment_condition",
                "date_recruitment",
            ]
            + [BaseCoreSerializer.Meta.fields[1]]
            + [BaseCoreSerializer.Meta.fields[2]]
        )

    def get_time_spent(self, obj: Recruitment) -> timedelta:
        """
        Calculate and return the total time spent on interviews.

        Args:
            obj (Recruitment): The instance of the Recruitment model.

        Returns:
            timedelta: The total time spent on interviews.
            and we convert timedelta to str format
        """
        return obj.interview_spent_time_calculate()

    def validate(self, data):
        """
        Validate the dates related to the recruitment process to ensure
        logical consistency.


        About validate date_recruiment and condition of recruiment:
            Someone whose recruitment_condition is rejected or non_accepted should not have date_recruiment

        The following conditions are checked abour number of resume:
        - The date when the resume was checked should not be more
          the date when it was received.
        - The date when the resume was approved should not be more
          the date when it was checked.
        - The date when the resume was interviewed should not be more
          the date when it was approved.

        Args:
            data (dict): A dictionary containing the data to validate.
                Someone whose recruitment_condition status is rejected or accepted should not have employment history
        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If any of the date conditions
                                          are not met.
        """
        received_resume = data.get("received_resume")
        checked_resume = data.get("checked_resume")
        approved_resume = data.get("approved_resume")
        interviewed_resume = data.get("interviewed_resume")
        recruitment_condition = data.get("recruitment_condition")
        date_recruitment = data.get("date_recruitment")
        now = timezone.now().date()

        if received_resume < checked_resume:
            raise serializers.ValidationError(
                "Checked resume number cannot be bigger than received resume number"
            )

        if checked_resume < approved_resume:
            raise serializers.ValidationError(
                "Approved resume number cannot be bigger than checked resume number"
            )

        if approved_resume < interviewed_resume:
            raise serializers.ValidationError(
                "Interviewed resume number cannot be bigger than approved resume number"
            )

        if recruitment_condition not in ["Accept", "accept"]:
            if date_recruitment is not None:
                raise serializers.ValidationError(
                    "No conditions other than being accepted can have an employment date. Please leave it blank"
                )
        elif date_recruitment is None:
            raise serializers.ValidationError(
                "condition of Accept or accept must have date_recruitment"
            )
        elif date_recruitment is not None:
            if date_recruitment > now:
                raise serializers.ValidationError(
                    "date_recruitment can be in future but not more than one year!"
                )

        return data


class RecruitmentDetailSerializer(serializers.ModelSerializer):
    """
    It about detail,
    it all alike above class except,
    just show four fields
    """

    time_spent = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for configuring the Recruitment serializer.

        Attributes:
            model (Model): Specifies the model to be serialized.
            fields (list): List of model fields to be included in the serialization.
        """

        model = Recruitment
        fields = [
            "duration_every_interview",
            "recruitment_position",
            "recruitment_condition",
            "date_recruitment",
            "time_spent",
        ]

    def get_time_spent(self, obj: Recruitment) -> timedelta:
        """
        Calculate and return the total time spent on interviews.

        Args:
            obj (Recruitment): The instance of the Recruitment model.

        Returns:
            timedelta: The total time spent on interviews.
        """
        return obj.interview_spent_time_calculate()

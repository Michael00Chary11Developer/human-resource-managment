from datetime import timedelta
from uuid import uuid4

from django.db import models

from core.models import BaseModelDate

"""
The usage model is defined,
which includes a method for selecting interview times and
some fields for the model
"""


class Recruitment(BaseModelDate):
    """_summary_
    recruiment_id is the primary key. It fills automatically in format of uuid4
    """

    recruitment_id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    """
    Fields:
        recruitment_id (UUIDField): The primary key for the model, automatically filled by uuid4.
        received_resume (PositiveSmallIntegerField): Number of resumes received.
        checked_resume (PositiveSmallIntegerField): Number of resumes checked.
        approved_resume (PositiveSmallIntegerField): Number of resumes approved.
        interviewed_resume (PositiveSmallIntegerField): Number of resumes that went through interviews.
        duration_every_interview (DurationField): Duration of each interview, stored as a timedelta object.
        recruitment_position (CharField): The position being recruited for
        recruitment_level_position(CharField): The level of position example intern or junior or senior
        recruitment_condition (CharField): The current condition of the recruitment
        date_recruitment (DateField): The date of the recruitment if condition of is not in [accept,Accept]
        date filled cannot be filled

    Methods:
        __str__(): Returns a human-readable string representation of the recruitment instance.
        interview_spent_time_calculate(): Calculates the total time spent on interviews.
    """

    received_resume = models.PositiveSmallIntegerField()
    checked_resume = models.PositiveSmallIntegerField()
    approved_resume = models.PositiveSmallIntegerField()
    interviewed_resume = models.PositiveSmallIntegerField()
    duration_every_interview = models.DurationField()
    recruitment_position = models.CharField(max_length=50)
    recruitment_level_position = models.CharField(max_length=50)
    recruitment_condition = models.CharField(max_length=50)
    date_recruitment = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the Person object.
        Readable for date_recruitment and recruitment_condition
        """
        return f"{self.date_recruitment}\t{self.recruitment_condition}"

    def interview_spent_time_calculate(self) -> str:
        """
        Return str format of time delta
        1.get duration_every_interview and convert it to seconds set to convertor_int
        2.the number of interviews_resume multiply convertor_int
        3. and convert it to str format for show in time format
        4.return this result
        """
        convertor_int = int(self.duration_every_interview.total_seconds())
        total_seconds = self.interviewed_resume * convertor_int
        return str(timedelta(seconds=total_seconds))

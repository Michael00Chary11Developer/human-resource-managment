from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet

from core.views import BaseModelViewSet

from .models import Recruitment
from .serializers import RecruitmentDetailSerializer, RecruitmentSerializer

"""
RecruitmentViews and RecruitmentDetailViews handle CRUD operations and filtering of Recruitment data.

- RecruitmentViews: Handles general recruitment data.
    - Orders recruitment data by 'recruiment_id'.
    - Filters by 'recruitment_possition' if provided in the URL.

- RecruitmentDetailViews: Handles detailed recruitment data.
    - Filters by 'recruitment_condition' if provided in the URL.

viewset manage data by crud,get,put,push,get,get by pk,delete,patch
"""


class RecruitmentViews(BaseModelViewSet):
    """
    Viewset for managing general recruitment data.

    - Handles listing, creating, updating, and deleting Recruitment records.
    - Orders recruitment data by 'recruiment_id'.
    - If 'recruitment_possition' is provided in the URL, filters the queryset by that position.
    - Uses 'RecruitmentSerializer' to serialize the Recruitment model.
    """

    queryset = Recruitment.objects.select_related("user_id").order_by(
        "date_recruitment"
    )
    serializer_class = RecruitmentSerializer

    def get_queryset(self):
        """
        Filter recruitment records by current user and optionally by 'recruitment_position'.
        """
        # Get base queryset filtered by user
        queryset = super().get_queryset()

        recruitment_position = self.kwargs.get("recruitment_position")
        if recruitment_position:
            queryset = queryset.filter(recruitment_position=recruitment_position)
            if not queryset.exists():
                raise NotFound("Not found recruitment_position!!!")
            return queryset

        return queryset


class RecruitmentDetailViews(ModelViewSet):
    """
    Viewset for managing detailed recruitment data.

    - Handles detailed retrieval of recruitment data based on 'recruitment_condition'.
    - Orders recruitment data by 'recruiment_id'.
    - Uses 'RecruitmentDetailSerializer' to serialize the detailed Recruitment model.
    """

    queryset = (
        Recruitment.objects.select_related("user_id").order_by("date_recruitment").all()
    )
    serializer_class = RecruitmentDetailSerializer

    def get_queryset(self):
        """
        Filter recruitment records by current user and optionally by 'recruitment_condition'.
        """
        # Filter by current user first
        queryset = Recruitment.objects.filter(user_id=self.request.user)

        recruitment_condition = self.kwargs.get("recruitment_condition")
        if recruitment_condition:
            queryset = queryset.filter(recruitment_condition=recruitment_condition)
            if not queryset.exists():
                raise NotFound("Not Found recruitment_condition!!!")
            return queryset

        return queryset

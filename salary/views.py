from core.views import BaseModelViewSet

from .models import Salary
from .serializer import SalarySerializer


class SalaryViewSet(BaseModelViewSet):
    """
    ViewSet for managing Salary records.

    This ViewSet provides the standard actions to create, read, update,
    and delete Salary records for personnel.
    """

    queryset = Salary.objects.select_related("personnel", "user_id").order_by(
        "created_at"
    )
    serializer_class = SalarySerializer

    def get_queryset(self):
        """
        Filter salary records by current user to ensure data isolation.
        """
        return super().get_queryset()

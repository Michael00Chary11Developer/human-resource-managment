from core.views import BaseModelViewSet

from .models import Salary
from .serializer import SalarySerializer


class SalaryViewSet(BaseModelViewSet):
    """
    ViewSet for managing Salary records.

    This ViewSet provides the standard actions to create, read, update,
    and delete Salary records for personnel.
    """

    queryset = Salary.objects.select_related("personnel", "user_id").all()

    """
    The queryset that this view will operate on.
    It retrieves all Salary records from the database.
    """
    serializer_class = SalarySerializer

    """
    The serializer class used to serialize and deserialize Salary data.
    """

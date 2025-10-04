from rest_framework.exceptions import NotFound

from core.serializer import PersonnelGetAllDataSerializer
from core.views import BaseModelViewSet

from .models import Personnel
from .serializer import PersonnelSerializer


class PersonnelViewSet(BaseModelViewSet):
    """
    A viewset for viewing and editing Personnel instances.

    This viewset provides CRUD operations for personnel records and includes filtering
    options based on personnel's position and level.
    """

    queryset = Personnel.objects.select_related("user_id").order_by("created_at")
    serializer_class = PersonnelSerializer

    def get_queryset(self):
        """
        Filter personnel instances by current user and optionally by
        'position' and 'level_for_position' parameters.

        Returns:
            queryset: A filtered queryset of Personnel instances.

        Raises:
            NotFound: If no personnel are found with the specified position or level.
        """
        # Get base queryset filtered by user
        queryset = super().get_queryset()

        position = self.kwargs.get("position")
        level_for_position = self.kwargs.get("level_for_position")

        if position:
            queryset = queryset.filter(position=position)
            if not queryset.exists():
                raise NotFound(f"No personnel found with position: {position}")
            return queryset

        if level_for_position:
            queryset = queryset.filter(level_for_position=level_for_position)
            if not queryset.exists():
                raise NotFound("No personnel found with level")
            return queryset

        return queryset


class PersonnelGetAllViewSet(BaseModelViewSet):
    """
    Optimized viewset for getting all personnel data with related objects.
    Uses select_related and prefetch_related to minimize database queries.
    """

    queryset = (
        Personnel.objects.select_related("user_id")
        .prefetch_related("salaries", "number_of_personnel_ex")
        .order_by("created_at")
        .all()
    )
    serializer_class = PersonnelGetAllDataSerializer

    http_method_names = ["get"]

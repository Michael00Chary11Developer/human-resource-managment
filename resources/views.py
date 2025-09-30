from rest_framework.exceptions import NotFound

from core.views import BaseModelViewSet

from .models import Resources
from .serializers import ResourceSerializer

"""
ResourceView handles CRUD operations and filtering of resource data.

- ResourceView:
    - Handles general resource data, including listing, creating, updating, and deleting resources.
    - Filters resource data by 'asset_code' or 'resource_name' if provided in the URL.
    - Uses ResourceSerializer for serializing the resource data.
"""


class ResourceView(BaseModelViewSet):
    """
    Viewset for managing general resource data.

    - Handles listing, creating, updating, and deleting Resource records.
    - If 'asset_code' or 'resource_name' is provided in the URL, filters the queryset by those fields.
    - Uses 'ResourceSerializer' to serialize the Resource model.
    """

    queryset = Resources.objects.all()
    serializer_class = ResourceSerializer

    def get_queryset(self):
        """
        Overrides the default 'get_queryset' method to filter resources by 'asset_code' or 'resource_name'.

        Raises:
            NotFound: If the provided 'asset_code' or 'resource_name' does not exist in the database.
        """
        asset_code = self.kwargs.get("asset_code")
        if asset_code:
            queryset = Resources.objects.filter(asset_code=asset_code)
            if not queryset.exists():
                raise NotFound("Not Found!!")
            return queryset

        resource_name = self.kwargs.get("resource_name")
        if resource_name:
            queryset = Resources.objects.filter(resource_name=resource_name)
            if not queryset.exists():
                raise NotFound(f"{resource_name} is not found!")
            return queryset

        return super().get_queryset()

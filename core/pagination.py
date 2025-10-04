from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for the project.

    Features:
    - Default page size: 20 items
    - Configurable page size via query parameter
    - Maximum page size limit: 10000 items
    - Consistent pagination across all endpoints
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 10000

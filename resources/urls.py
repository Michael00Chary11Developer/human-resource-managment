from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ResourceView

"""
URL Configuration for Resource Management.

- DefaultRouter: Automatically generates URLs for the ResourceView (a ModelViewSet).
- register: Registers the ResourceView under the 'manage' prefix.

Optional URL Patterns:
    - asset-code/<int:asset_code>/: Custom route to filter resources by asset code.
    - resource-name/<str:resource_name>/: Custom route to filter resources by resource name.
"""

# Create a router instance
router = DefaultRouter()
router.register("manage", ResourceView)

# Define URL patterns
urlpatterns = [
    path("", include(router.urls)),
    path("asset-code/<int:asset_code>/", ResourceView.as_view({"get": "list"})),
    path("resource-name/<str:resource_name>/", ResourceView.as_view({"get": "list"})),
]

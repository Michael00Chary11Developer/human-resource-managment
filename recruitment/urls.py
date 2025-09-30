from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecruitmentDetailViews, RecruitmentViews

"""
URL Configuration for Recruitment API.

1. 'router': Creates the router for the 'RecruitmentViews' and automatically generates standard routes for it.
2. 'router.register': Registers the viewset with the router, handling all 'CRUD' operations under the "manage" path.
3. 'include(router.urls)': Includes all the automatically generated URLs from the router in the urlpatterns.
4. Additional paths are manually defined for filtering based on 'recruitment_condition' and 'recruitment_possition'.

Endpoints:
- 'manage/': Default CRUD operations for Recruitment.
- 'condition/<recruitment_condition>/': Filters recruitments by condition (GET request).
- 'possition/<recruitment_possition>/': Filters recruitments by position (GET request).
"""

# Initialize the router and register the viewset
router = DefaultRouter()
router.register("manage", RecruitmentViews, basename="RecruitmentRouter")

# Define urlpatterns
urlpatterns = [
    # Include the automatically created router URLs
    path("", include(router.urls)),
    # Custom path to filter by recruitment condition
    path(
        "condition/<str:recruitment_condition>/",
        RecruitmentDetailViews.as_view({"get": "list"}),
    ),
    # Custom path to filter by recruitment position
    path(
        "position/<str:recruitment_position>/",
        RecruitmentViews.as_view({"get": "list"}),
    ),
]

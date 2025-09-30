from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("manage", views.PersonnelViewSet, basename="personnel")
router_for_get_all_detail = DefaultRouter()
router_for_get_all_detail.register("", views.PersonnelGetAllViewSet, basename="get-all")


urlpatterns = [
    path("", include(router.urls)),
    path("get-all/", include(router_for_get_all_detail.urls), name="get_all"),
    path(
        "possition/<str:position>/",
        views.PersonnelViewSet.as_view({"get": "list"}),
        name="position",
    ),
    path(
        "level/<str:level_for_position>/",
        views.PersonnelViewSet.as_view({"get": "list"}),
        name="level_for_position",
    ),
]

"""
This module contains URL patterns for the personnel app.

- Router:
    - A router is used to automatically generate URL patterns for the PersonnelViewSet.

- ViewSet Registration:
    - PersonnelViewSet is registered with the prefix 'manage'.
    - This ViewSet provides CRUD (Create, Read, Update, and Delete) operations for personnel records.

- URL Patterns:
    - Includes all generated URL patterns for managing personnel.
    - Additional paths for filtering personnel by position and level are included.
    - The path 'position/<str:position>/' allows listing personnel based on their position.
    - The path 'level/<str:level_for_position>/' allows listing personnel based on their level.
"""

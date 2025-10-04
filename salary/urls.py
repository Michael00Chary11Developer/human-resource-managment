from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("manage", views.SalaryViewSet, basename="salary")

urlpatterns = [
    path("", include(router.urls)),
]

"""
This module contains URL patterns for the salary app.

- Router:
    - A router is used to automatically generate URL patterns for the SalaryViewSet.

- ViewSet Registration:
    - SalaryViewSet is registered with the prefix 'manage'.
    - This ViewSet provides CRUD (Create, Read, Update, and Delete) operations for salary records.

- URL Patterns:
    - Includes all generated URL patterns for managing salaries.
"""

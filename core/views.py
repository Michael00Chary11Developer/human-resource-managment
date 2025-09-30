from django.contrib.auth.models import User
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base viewset to handle user_id assignment on create.
    """

    def perform_create(self, serializer):
        """
        Override to add the user_id to the instance.
        """

        if self.request.user.is_authenticated:
            serializer.save(user_id=self.request.user)
        else:
            try:
                default_user = User.objects.get(pk=1)
                serializer.save(user_id=default_user)
            except User.DoesNotExist:
                raise NotFound("Default user not found.")

    def get_queryset(self):
        """
        Optimize queryset with select_related and prefetch_related
        to reduce database queries.
        """
        query_set = super().get_queryset()

        limit = self.request.query_params.get("limit")
        offset = self.request.query_params.get("offset")

        if limit is not None:
            self.pagination_class = LimitOffsetPagination
            self.pagination_class.default_limit = int(limit)

        if limit is not None or offset is not None:
            self.pagination_class = LimitOffsetPagination

        return query_set


"""
two authentication class that create login base on basic_authentication:
    1:swagger
    2.redoc

"""


@permission_classes([IsAdminUser])
@authentication_classes([BasicAuthentication])
class SwaggerViewBasicAuthentication(SpectacularSwaggerView):
    """
    Requires admin access and uses Basic Authentication.
    """


@permission_classes([IsAdminUser])
@authentication_classes([BasicAuthentication])
class RedocViewBasicAuthentication(SpectacularRedocView):
    """
    Requires admin access and uses Basic Authentication.
    """

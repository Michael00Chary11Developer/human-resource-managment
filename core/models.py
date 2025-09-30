from django.contrib.auth.models import User
from django.db import models

"""
class:
    BaseModelDate abstract Model,
"""


class BaseModelDate(models.Model):
    """
    user id is id if one superuser that is 1
    handle date for vreate and update automatically
    """

    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    """
    Meta:
        show that this class is abstract
        and not migrate in database
    """

    class Meta:
        abstract = True

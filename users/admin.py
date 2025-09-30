from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User admin with additional fields.
    """

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_hr_manager",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "is_hr_manager",
        "is_active",
        "is_staff",
        "date_joined",
        "department",
    )
    search_fields = ("email", "username", "first_name", "last_name", "phone_number")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Work info", {"fields": ("department", "position", "is_hr_manager")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_hr_manager",
                ),
            },
        ),
    )

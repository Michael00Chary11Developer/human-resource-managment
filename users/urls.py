from django.urls import path

from . import views

urlpatterns = [
    # Authentication endpoints
    path("register/", views.UserRegistrationView.as_view(), name="user-register"),
    path("login/", views.login_view, name="user-login"),
    path("logout/", views.logout_view, name="user-logout"),
    # Profile and user management
    path("profile/", views.UserProfileView.as_view(), name="user-profile"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("list/", views.UserListView.as_view(), name="user-list"),
]

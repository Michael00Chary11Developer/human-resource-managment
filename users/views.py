from django.contrib.auth import login, logout
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "user": UserProfileSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        login(request, user)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",
                "user": UserProfileSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint.
    """
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view - get and update profile.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change password endpoint.
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    """
    List all users (HR managers only).
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only HR managers can see all users
        if not self.request.user.is_hr_manager:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

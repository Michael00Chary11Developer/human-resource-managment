from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "department",
            "position",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password.")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "department",
            "position",
            "is_hr_manager",
            "is_active",
            "date_joined",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "date_joined", "created_at", "updated_at"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "department", "position"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    """

    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

from rest_framework import serializers
from users_auth_app.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.

    Fields:
    - fullname: Full name of the user
    - email: User email (unique)
    - password: Password (write-only)
    - repeated_password: Password confirmation (write-only)

    Validates that password and repeated_password match.
    """

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("fullname", "email", "password", "repeated_password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):

        """
        Check that password and repeated_password match.
        """
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):

    """
    Serializer for user login.

    Fields:
    - email: User email
    - password: User password (write-only)

    Validates that the credentials match an existing user.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid credentials.")

        data["user"] = user
        return data
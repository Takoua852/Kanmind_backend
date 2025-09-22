from rest_framework import serializers
from django.contrib.auth import authenticate
from users_auth_app.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("fullname", "email", "password", "repeated_password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        return data

    def create(self, validated_data):
        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Ungültige Zugangsdaten.")
        data["user"] = user
        return data


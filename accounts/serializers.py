from rest_framework import serializers # type: ignore
from core.mixins import UserAdminFieldsMixin
from .models import User

class UserSerializer(UserAdminFieldsMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "role", "document_id", "phone", "is_verified",
            "is_active", "is_staff", "last_login", "date_joined",
            "password",
        )
        read_only_fields = ("id", "last_login", "date_joined")
        extra_kwargs = {"email": {"required": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        user.set_password(password) 
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

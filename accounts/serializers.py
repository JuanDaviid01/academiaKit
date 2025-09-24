from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Nunca se devuelve; solo se usa para crear/actualizar
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        # Lista explícita (¡no uses '__all__' en usuarios!)
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "role", "document_id", "phone", "is_verified",
            "is_active", "is_staff", "last_login", "date_joined",
            "password",
        )
        read_only_fields = ("id", "last_login", "date_joined")
        extra_kwargs = {
            "email": {"required": True},         
            "is_staff": {"required": False},
            "is_active": {"required": False},
        }

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if not request or not request.user.is_staff:
            # Nadie que no sea admin puede tocar estos campos
            fields["is_staff"].read_only = True
            fields["is_active"].read_only = True
            fields["role"].read_only = True
        return fields

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
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

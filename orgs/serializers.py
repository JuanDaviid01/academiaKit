from academiaKit.core.mixins import AdminFieldsMixin
from rest_framework import serializers # type: ignore
from .models import Institution, Campus, Building, Room

class InstitutionSerializer(AdminFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"   # <- “todos los campos del modelo”

class CampusSerializer(AdminFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = "__all__"

class BuildingSerializer(AdminFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"

class RoomSerializer(AdminFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
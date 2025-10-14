from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from .models import Institution, Campus, Building, Room
from .serializers import InstitutionSerializer, CampusSerializer, BuildingSerializer, RoomSerializer
# Create your views here.

# para interactuar se requiere autenticacion
# modificarlos solo para le admin
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all().order_by("name")
    serializer_class = InstitutionSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filtros y utilidades
    search_fields = ("name", "code")
    ordering_fields = ("name", "code", "created_at", "updated_at")
    filterset_fields = ("is_active", "country")


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.select_related("institution").all().order_by(
        "institution__name", "name"
    )
    serializer_class = CampusSerializer
    permission_classes = [IsAdminOrReadOnly]

    search_fields = ("name", "code", "city", "institution__name", "institution__code")
    ordering_fields = ("name", "code", "city", "created_at", "updated_at")
    filterset_fields = ("is_active", "institution")


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.select_related("campus", "campus__institution").all().order_by(
        "campus__institution__name", "campus__name", "name"
    )
    serializer_class = BuildingSerializer
    permission_classes = [IsAdminOrReadOnly]

    search_fields = ("name", "code", "campus__name", "campus__institution__name")
    ordering_fields = ("name", "code", "floors", "created_at", "updated_at")
    filterset_fields = ("is_active", "campus")


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related(
        "building", "building__campus", "building__campus__institution"
    ).all().order_by(
        "building__campus__institution__name",
        "building__campus__name",
        "building__name",
        "code",
    )
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    search_fields = (
        "name", "code",
        "building__name",
        "building__campus__name",
        "building__campus__institution__name",
    )
    ordering_fields = ("code", "name", "capacity", "created_at", "updated_at")
    filterset_fields = ("is_active", "building")
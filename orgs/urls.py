from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutionViewSet,CampusViewSet,BuildingViewSet,RoomViewSet

#router para orgs
router = DefaultRouter()
router.register(r"institutions", InstitutionViewSet, basename="institution")
router.register(r"campuses", CampusViewSet, basename="campus")
router.register(r"buildings", BuildingViewSet, basename="building")
router.register(r"rooms", RoomViewSet, basename="room")

urlpatterns = [
    path("", include(router.urls)),
]

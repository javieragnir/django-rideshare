from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RideEventViewSet, RideViewSet

router = DefaultRouter()
router.register(r"rides", RideViewSet, basename="ride")
router.register(r"ride-events", RideEventViewSet, basename="ride_event")

urlpatterns = [
    path("", include(router.urls)),
]

from rest_framework import viewsets

from config.permissions import AdminOnlyPermission

from .models import Ride, RideEvent
from .serializers import RideEventSerializer, RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOnlyPermission]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer


class RideEventViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOnlyPermission]
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer

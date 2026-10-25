from rest_framework import viewsets
from rest_framework.response import Response

from config.permissions import AdminOnlyPermission

from .filters import RideFilter
from .models import Ride, RideEvent
from .serializers import RideEventSerializer, RideListSerializer, RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOnlyPermission]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    filterset_class = RideFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RideListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RideListSerializer(queryset, many=True)
        return Response(serializer.data)


class RideEventViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOnlyPermission]
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer

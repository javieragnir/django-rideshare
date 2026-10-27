from django.db.models import F, Prefetch, Value
from django.db.models.functions import ACos, Cos, Radians, Sin
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
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

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            earliest_time = timezone.now() - timezone.timedelta(hours=24)
            queryset = queryset.prefetch_related(
                Prefetch(
                    "events",
                    queryset=RideEvent.objects.filter(created_at__gte=earliest_time),
                    to_attr="todays_ride_events",
                )
            )

            order_params = self.request.query_params.get("o")
            order_params = order_params.split(",") if order_params else []

            if "distance" not in order_params:
                return queryset

            latitude = self.request.query_params.get("latitude")
            longitude = self.request.query_params.get("longitude")

            if latitude is None or longitude is None:
                raise ValidationError(
                    {
                        "distance": "Must include latitude and longitude parameters when ordering by distance"
                    }
                )

            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                raise ValidationError(
                    {"distance": "Latitude and longitude parameters must be floats"}
                )

            # Adapted from https://djangosnippets.org/snippets/10854/
            return queryset.annotate(
                distance=ACos(
                    Cos(Radians(Value(latitude)))
                    * Cos(Radians(F("pickup_latitude")))
                    * Cos(Radians(F("pickup_longitude")) - Radians(Value(longitude)))
                    + Sin(Radians(Value(latitude))) * Sin(Radians(F("pickup_latitude")))
                )
                * 3959
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RideListSerializer

        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RideEventViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOnlyPermission]
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer

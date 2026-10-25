from django.db.models import ExpressionWrapper, F, FloatField, Prefetch, Value
from django.db.models.functions import (
    ASin,
    Cos,
    Least,
    Power,
    Radians,
    Sin,
    Sqrt,
)
from django.utils import timezone
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

            latitude = self.request.query_params.get("latitude")
            longitude = self.request.query_params.get("longitude")

            if latitude is None or longitude is None:
                return queryset

            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError:
                return queryset.none()

            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                return queryset.none()

            lat1 = Radians(F("pickup_latitude"))
            lat2 = Radians(Value(latitude))
            lon1 = Radians(F("pickup_latitude"))
            lon2 = Radians(Value(longitude))

            a = Power(Sin((lat1 - lat2) / 2.0), 2) + Cos(lat1) * Cos(lat2) * Power(
                Sin((lon1 - lon2) / 2.0), 2
            )

            distance = ExpressionWrapper(
                6371.0 * 2.0 * ASin(Sqrt(Least(Value(1.0), a))),
                output_field=FloatField(),
            )

            return queryset.annotate(distance=distance)

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

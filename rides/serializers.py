from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ride, RideEvent

User = get_user_model()


class RideEventSerializer(serializers.ModelSerializer):
    ride = serializers.PrimaryKeyRelatedField(queryset=Ride.objects.all())

    class Meta:
        model = RideEvent
        fields = [
            "id",
            "ride",
            "description",
            "created_at",
        ]


class RideSerializer(serializers.ModelSerializer):
    rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    driver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Ride
        fields = [
            "id",
            "rider",
            "driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
        ]


class RideListSerializer(serializers.ModelSerializer):
    id_rider = serializers.PrimaryKeyRelatedField(
        source="rider",
        queryset=User.objects.all(),
    )
    id_driver = serializers.PrimaryKeyRelatedField(
        source="driver",
        queryset=User.objects.all(),
    )
    events = RideEventSerializer(many=True, read_only=True)

    class Meta:
        model = Ride
        read_only_fields = ["events"]
        fields = [
            "id",
            "id_rider",
            "id_driver",
            "events",
        ]

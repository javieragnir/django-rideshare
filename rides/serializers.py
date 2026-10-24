from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ride, RideEvent

User = get_user_model()


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

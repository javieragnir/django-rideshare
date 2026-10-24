from rest_framework import serializers

from .models import Ride, RideEvent


class RideSerializer(serializers.ModelSerializer):
    rider = serializers.PrimaryKeyRelatedField()
    driver = serializers.PrimaryKeyRelatedField()

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
    ride = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = RideEvent
        fields = [
            "id",
            "ride",
            "description",
            "created_at",
        ]

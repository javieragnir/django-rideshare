from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class Ride(models.Model):
    STATUS_CHOICES = Choices(
        ("En-route", "en_route", _("En-route")),
        ("Pickup", "pickup", _("Pickup")),
        ("Dropoff", "dropoff", _("Dropoff")),
    )

    id = models.BigAutoField(primary_key=True, db_column="id_ride")

    rider = models.ForeignKey(
        "users.User",
        verbose_name=_("rider"),
        db_column="id_rider",
        related_name="rider_rides",
        on_delete=models.CASCADE,
    )

    driver = models.ForeignKey(
        "users.User",
        verbose_name=_("driver"),
        db_column="id_driver",
        related_name="driver_rides",
        on_delete=models.CASCADE,
    )

    pickup_latitude = models.FloatField(
        verbose_name=_("pickup latitude"),
        db_column="pickup_latitude",
    )

    pickup_longitude = models.FloatField(
        verbose_name=_("pickup longitude"),
        db_column="pickup_longitude",
    )

    dropoff_latitude = models.FloatField(
        verbose_name=_("dropoff latitude"),
        db_column="dropoff_latitude",
    )

    dropoff_longitude = models.FloatField(
        verbose_name=_("dropoff longitude"),
        db_column="dropoff_longitude",
    )

    pickup_time = models.DateTimeField(
        verbose_name=_("pickup Time"), db_column="pickup_time"
    )

    class Meta:
        verbose_name = _("ride")
        verbose_name_plural = _("rides")
        db_table = "rides"

    def __str__(self):
        return f"D: {self.driver}, R: {self.rider} - {self.pickup_time}"


class RideEvent(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="id_ride_event")

    ride = models.ForeignKey(
        "Ride",
        verbose_name="Ride",
        db_column="id_ride",
        related_name="events",
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        _("description"), max_length=2000, db_column="description"
    )

    created_at = models.DateTimeField(
        verbose_name=_("created at"), db_column="created_at", auto_now_add=True
    )

    class Meta:
        verbose_name = _("ride event")
        verbose_name_plural = _("ride events")
        db_table = "ride_events"

    def __str__(self):
        return f"{self.ride} - {self.created_at}"

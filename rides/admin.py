from django.contrib import admin

from .models import Ride, RideEvent


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    search_fields = ["rider", "driver"]
    list_filter = ["rider", "driver"]
    list_display = [
        "id",
        "rider",
        "driver",
        "pickup_time",
    ]


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    search_fields = ["ride"]
    list_display = [
        "ride",
        "created_at",
    ]

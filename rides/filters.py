import django_filters

from .models import Ride


class RideFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(
        field_name="rider__email",
        lookup_expr="icontains",
    )

    o = django_filters.filters.OrderingFilter(
        fields=(
            ("pickup_time", "pickup_time"),
            ("distance", "distance"),
        ),
    )

    class Meta:
        model = Ride
        fields = ["status", "email"]

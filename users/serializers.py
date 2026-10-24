from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "first_name",
            "last_name",
            "phone_number",
            "is_active",
            "is_staff",
        ]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("is_active", "role", "is_staff", "is_superuser")

    search_fields = ("email", "first_name", "last_name")

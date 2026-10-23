from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = Choices(
        ("Standard", "standard", _("Standard")),
        ("Admin", "admin", _("Admin")),
    )

    id = models.BigAutoField(primary_key=True, db_column="id_user")

    role = models.CharField(
        _("type"),
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES.standard,
        max_length=16,
        db_column="role",
    )

    first_name = models.CharField(
        _("first name"), max_length=150, db_column="first_name"
    )
    last_name = models.CharField(_("last name"), max_length=150, db_column="last_name")

    email = models.EmailField(
        _("email"), max_length=255, db_column="email", unique=True
    )

    phone_number = PhoneNumberField(
        verbose_name=_("mobile number"),
        db_column="application_phone",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"

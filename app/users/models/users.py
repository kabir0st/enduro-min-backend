from uuid import uuid4
from core.utils.functions import default_json

from core.utils.models import TimeStampedModel
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


def default_array():
    return []


class UserbaseManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


def image_directory_path(instance, filename):
    return "users/{0}/profile_image.jpg".format(instance.email)


class UserBase(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    stripe_customer_id = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)

    phone_number = models.CharField(max_length=15, default='', blank=True)

    gender = models.CharField(max_length=8, default='')
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(default='', blank=True)
    zip_code = models.CharField(max_length=10, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    BLOOD_GROUPS = (('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                    ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
                    ('unknown', 'Unknown'))
    blood_group = models.CharField(max_length=7,
                                   choices=BLOOD_GROUPS,
                                   default='unknown')
    profile_image = models.ImageField(upload_to=image_directory_path,
                                      null=True,
                                      blank=True)

    distance_ran = models.DecimalField(default=0.0,
                                       max_digits=60,
                                       decimal_places=2)
    event_participated_in_count = models.PositiveIntegerField(default=0)
    indexes = models.JSONField(default=default_json, blank=True)
    preferred_size = models.CharField(max_length=255, default='', blank=True)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    designation = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserbaseManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        ordering = ["-id"]

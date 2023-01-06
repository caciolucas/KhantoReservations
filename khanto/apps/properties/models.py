from django.db import models

from common.models import AutoTimestampModel, UUIDModel
from django.db.models.signals import post_migrate
from django.core.management import call_command

# Create your models here.


class Property(AutoTimestampModel, UUIDModel):
    code = models.CharField(max_length=10, unique=True)
    max_guests = models.IntegerField()
    n_bathrooms = models.IntegerField()
    is_pet_friendly = models.BooleanField()
    clean_price = models.DecimalField(max_digits=10, decimal_places=2)
    activation_date = models.DateField()

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Announcement(AutoTimestampModel, UUIDModel):
    AIRBNB = "airbnb"
    BOOKING = "booking"
    SEAZONE = "seazone"
    OTHER = "other"

    PLATFORM_CHOICES = (
        (AIRBNB, "AirBnb"),
        (BOOKING, "Booking"),
        (SEAZONE, "Seazone"),
        (OTHER, "Other"),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    # Ideally this should be a foreign key to a platform model that has a name and a fee
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["property__code", "platform"]

    def __str__(self):
        return f"{self.property.code} - {self.platform}"

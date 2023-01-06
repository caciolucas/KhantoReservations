from django.db import models
from common.models import AutoTimestampModel, UUIDModel
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_migrate
from common.utils import get_random_string
from django.core.management import call_command
from rest_framework.exceptions import ValidationError

# Create your models here.


class Reservation(AutoTimestampModel, UUIDModel):
    code = models.CharField(max_length=10, unique=True)
    announcement = models.ForeignKey(
        "properties.Announcement", on_delete=models.CASCADE
    )
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    n_guests = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "announcement"]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if self.checkin_date >= self.checkout_date:
            raise ValidationError("Checkin date must be before checkout date")
        if self.announcement.property.max_guests < self.n_guests:
            raise ValidationError("Number of guests exceeds maximum")

        super().save(*args, **kwargs)


@receiver(pre_save, sender=Reservation)
def reservation_pre_save_receiver(sender, **kwargs):
    instance = kwargs["instance"]
    if not instance.code:
        instance.code = get_random_string(length=10)

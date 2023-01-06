from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from properties.models import Announcement

from reservations.models import Reservation
from properties.serializers import AnnouncementSerializer


class ReservationSerializer(serializers.ModelSerializer):
    announcement = AnnouncementSerializer(read_only=True)
    announcement_id = serializers.UUIDField(write_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"

    def validate(self, data):
        errors = {}

        checkin_date = data["checkin_date"]
        checkout_date = data["checkout_date"]
        if checkin_date >= checkout_date:
            errors.update({"checkin_date": "Checkin date must be before checkout date"})

        try:
            announcement = Announcement.objects.get(id=data["announcement_id"])

            if announcement.property.max_guests < data["n_guests"]:
                errors.update({"n_guests": "Number of guests exceeds maximum"})

        except Announcement.DoesNotExist:
            errors.update(
                {"announcement_id": "Announcement with this id does not exist"}
            )

        if errors:
            raise ValidationError(errors)

        return data

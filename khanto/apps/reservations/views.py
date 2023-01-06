from reservations.serializers import ReservationSerializer
from reservations.models import Reservation
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from common.views import NoUpdateModelViewSet

# Create your views here.


class ReservationViewSet(NoUpdateModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

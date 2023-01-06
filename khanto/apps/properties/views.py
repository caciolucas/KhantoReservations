from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from properties.models import Announcement, Property
from properties.serializers import AnnouncementSerializer, PropertySerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import filters
from common.views import NoDeleteModelViewSet

# Create your views here.


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filterset_fields = {
        "code": ["icontains"],
        "max_guests": ["exact", "lte", "gte"],
    }


class AnnouncementViewSet(NoDeleteModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    filterset_fields = {
        "property__code": ["icontains"],
        "platform": ["exact"],
    }

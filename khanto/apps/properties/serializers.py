from rest_framework import serializers

from properties.models import Announcement, Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    property_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"

    def create(self, validated_data):
        try:
            Property.objects.get(id=validated_data["property_id"])
        except Property.DoesNotExist:
            raise serializers.ValidationError(
                {"property_id": "Property does not exist"}
            )
        return super().create(validated_data)

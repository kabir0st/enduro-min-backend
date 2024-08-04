from rest_framework import serializers

from events.models import (EventType, EventTag)


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = '__all__'


class EventTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventTag
        fields = '__all__'

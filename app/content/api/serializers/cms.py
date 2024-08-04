from content.models.cms import (HighLightEvents, HomePageLogo, TeamMember,
                                Testimonial)
from core.utils.serializers import Base64ImageField
from events.api.serializers.event import EventSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class TestimonialSerializer(ModelSerializer):

    logo = Base64ImageField()

    class Meta:
        model = Testimonial
        fields = '__all__'


class HomePageLogoSerializer(ModelSerializer):

    logo = Base64ImageField(required=True)

    class Meta:
        model = HomePageLogo
        fields = '__all__'


class TeamMemberSerializer(ModelSerializer):

    photo = Base64ImageField()

    class Meta:
        model = TeamMember
        fields = '__all__'


class HighLightEventsSerializer(ModelSerializer):

    main_event_detail = SerializerMethodField()
    carousel_events_details = SerializerMethodField()

    def get_main_event_detail(self, obj):
        if obj.main_event:
            return EventSerializer(instance=obj.main_event).data
        return {}

    def get_carousel_events_details(self, obj):
        if obj.carousel_events:
            return EventSerializer(instance=obj.carousel_events.all(),
                                   many=True).data
        return {}

    class Meta:
        model = HighLightEvents
        fields = '__all__'

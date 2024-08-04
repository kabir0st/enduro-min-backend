from core.utils.serializers import Base64FileField, Base64ImageField
from events.models import (AddonTemplate, CategoryTemplate, EventTemplate,
                           FAQTemplate, MediaForEventTemplate, PrizeTemplate,
                           MediaForCategoryTemplate, MediaForAddonTemplate)
from rest_framework import serializers

from events.models.event_templates import ScheduleTemplate

from .event_utils import EventTagSerializer, EventTypeSerializer


class EventTemplateSerializer(serializers.ModelSerializer):

    headline_image = Base64ImageField(required=False, allow_null=True)
    header_route_image = Base64ImageField(required=False, allow_null=True)
    gpx_file = Base64FileField(required=False, allow_null=True)
    logo = Base64FileField(required=False, allow_null=True)

    event_tags_details = EventTagSerializer(source='event_tags',
                                            many=True,
                                            read_only=True)
    event_type_detail = EventTypeSerializer(source='event_type',
                                            read_only=True)

    class Meta:
        model = EventTemplate
        fields = '__all__'


class MediaForEventTemplateSerializer(serializers.ModelSerializer):
    src = Base64ImageField(required=True)

    class Meta:
        model = MediaForEventTemplate
        fields = '__all__'


class AddonTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddonTemplate
        fields = '__all__'


class MediaForAddonTemplateSerializer(serializers.ModelSerializer):
    src = Base64ImageField(required=True)

    class Meta:
        model = MediaForAddonTemplate
        fields = '__all__'


class FAQTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQTemplate
        fields = '__all__'


class PrizeTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrizeTemplate
        fields = '__all__'


class CategoryTemplateSerializer(serializers.ModelSerializer):

    headline_image = Base64ImageField(required=False, allow_null=True)
    gpx_file = Base64FileField(required=False, allow_null=True)
    prizes_details = serializers.SerializerMethodField()

    def get_prizes_details(self, obj):
        return PrizeTemplateSerializer(
            obj.template_prizes.all(),
            many=True,
            read_only=True,
            context={
                "request": self.context["request"]
            },
        ).data

    class Meta:
        model = CategoryTemplate
        fields = '__all__'


class MediaForCategoryTemplateSerializer(serializers.ModelSerializer):
    src = Base64ImageField(required=True)

    class Meta:
        model = MediaForCategoryTemplate
        fields = '__all__'


class ScheduleTemplateSerializer(serializers.ModelSerializer):

    headline = Base64ImageField(required=False, allow_null=True)
    gpx_file = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = ScheduleTemplate
        fields = '__all__'


class DetailedEventTemplateSerializer(EventTemplateSerializer):
    schedule_details = serializers.SerializerMethodField()

    addons = serializers.SerializerMethodField()
    faqs = serializers.SerializerMethodField()
    event_categories = serializers.SerializerMethodField()

    def get_schedule_details(self, obj):
        return ScheduleTemplateSerializer(
            obj.template_schedules.filter().order_by('-id'),
            many=True,
            read_only=True,
        ).data

    def get_addons(self, obj):
        return AddonTemplateSerializer(
            obj.template_addons.all(),
            many=True,
            read_only=True,
            context={
                "request": self.context["request"]
            },
        ).data

    def get_faqs(self, obj):
        return FAQTemplateSerializer(
            obj.template_faqs.all(),
            many=True,
            read_only=True,
            context={
                "request": self.context["request"]
            },
        ).data

    def get_event_categories(self, obj):
        return CategoryTemplateSerializer(
            obj.template_categories.all(),
            many=True,
            read_only=True,
            context={
                "request": self.context["request"]
            },
        ).data

    class Meta:
        model = EventTemplate
        fields = '__all__'

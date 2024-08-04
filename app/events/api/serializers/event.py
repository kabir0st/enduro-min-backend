from core.utils.serializers import Base64FileField, Base64ImageField
from events.models import (FAQ, Addon, Category, Event, MediaForEvent, Prize,
                           Schedule)
from events.models.event import (MediaForAddon, MediaForCategory, ResultEntry,
                                 ResultList)
from rest_framework import serializers

from .event_utils import EventTagSerializer, EventTypeSerializer


class MediaForEventSerializer(serializers.ModelSerializer):
    src = Base64ImageField(required=True)

    class Meta:
        model = MediaForEvent
        fields = '__all__'


class MediaForCategorySerializer(serializers.ModelSerializer):
    src = Base64ImageField(required=True)

    class Meta:
        model = MediaForCategory
        fields = '__all__'


class MiniCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    headline_image = Base64ImageField(required=False, allow_null=True)
    header_route_image = Base64ImageField(required=False, allow_null=True)
    gpx_file = Base64FileField(required=False, allow_null=True)
    logo = Base64FileField(required=False, allow_null=True)

    event_tags_details = EventTagSerializer(source='event_tags',
                                            many=True,
                                            read_only=True)
    event_type_detail = EventTypeSerializer(source='event_type',
                                            read_only=True)
    is_registration_open = serializers.SerializerMethodField()

    category_details = serializers.SerializerMethodField()

    def get_category_details(self, obj):
        return MiniCategorySerializer(obj.categories.filter().order_by('-id'),
                                      many=True).data

    def get_is_registration_open(self, obj):
        return obj.is_registration_open

    class Meta:
        model = Event
        fields = '__all__'


class MediaForAddonSerializer(serializers.ModelSerializer):
    src = Base64ImageField(required=True)

    class Meta:
        model = MediaForAddon
        fields = '__all__'


class AddonSerializer(serializers.ModelSerializer):
    medias = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Addon
        fields = '__all__'

    def get_medias(self, obj):
        return MediaForAddonSerializer(obj.medias.filter().order_by('-id'),
                                       many=True).data


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = '__all__'


class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    headline_image = Base64ImageField(required=False, allow_null=True)
    gpx_file = Base64FileField(required=False, allow_null=True)
    prizes_details = serializers.SerializerMethodField()

    def get_prizes_details(self, obj):
        return PrizeSerializer(
            obj.prizes.all(),
            many=True,
            read_only=True,
        ).data

    class Meta:
        model = Category
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):

    headline = Base64ImageField(required=False, allow_null=True)
    gpx_file = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = Schedule
        fields = '__all__'


class DetailedEventSerializer(EventSerializer):

    schedule_details = serializers.SerializerMethodField()
    addon_details = serializers.SerializerMethodField()
    category_details = serializers.SerializerMethodField()
    faq_details = serializers.SerializerMethodField()
    category_details = serializers.SerializerMethodField()

    def get_schedule_details(self, obj):
        return ScheduleSerializer(
            obj.schedules.filter().order_by('-id'),
            many=True,
            read_only=True,
        ).data

    def get_addon_details(self, obj):
        return AddonSerializer(
            obj.addons.filter().order_by('-id'),
            many=True,
            read_only=True,
        ).data

    def get_category_details(self, obj):
        return CategorySerializer(
            obj.categories.filter().order_by('-id'),
            many=True,
            read_only=True,
        ).data

    def get_faq_details(self, obj):
        return FAQSerializer(
            obj.faqs.filter().order_by('-id'),
            many=True,
            read_only=True,
        ).data

    class Meta:
        model = Event
        fields = '__all__'


class ResultListEntrySerializer(serializers.Serializer):

    class Meta:
        model = ResultEntry
        fields = '__all__'


class ResultListSerializer(serializers.Serializer):

    class Meta:
        model = ResultList
        fields = '__all__'


class ResultEntrySerializer(serializers.Serializer):

    class Meta:
        model = ResultEntry
        fields = '__all__'

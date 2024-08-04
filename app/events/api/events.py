from core.permissions import IsAdminOrReadOnly
from core.utils.functions import InfinitePagination
from core.utils.viewsets import DefaultViewSet
from django_filters import rest_framework as filters
from events.models import FAQ, Addon, Category, Event, Prize
from events.models.event import (MediaForAddon, MediaForCategory,
                                 MediaForEvent, ResultEntry, ResultList,
                                 Schedule)

from .serializers.event import (
    AddonSerializer, CategorySerializer, DetailedEventSerializer,
    EventSerializer, FAQSerializer, MediaForAddonSerializer,
    MediaForCategorySerializer, MediaForEventSerializer, PrizeSerializer,
    ResultEntrySerializer, ResultListSerializer, ScheduleSerializer)


class CustomFilter(filters.FilterSet):
    created_at_gte = filters.IsoDateTimeFilter(field_name="created_at",
                                               lookup_expr='gte')
    created_at_lte = filters.IsoDateTimeFilter(field_name="created_at",
                                               lookup_expr='lte')

    start_datetime_gte = filters.IsoDateTimeFilter(field_name="start_datetime",
                                                   lookup_expr='gte')
    start_datetime_lte = filters.IsoDateTimeFilter(field_name="start_datetime",
                                                   lookup_expr='lte')

    end_datetime_gte = filters.IsoDateTimeFilter(field_name="end_datetime",
                                                 lookup_expr='gte')
    end_datetime_lte = filters.IsoDateTimeFilter(field_name="end_datetime",
                                                 lookup_expr='lte')

    open_registration_from_gte = filters.IsoDateTimeFilter(
        field_name="open_registration_from", lookup_expr='gte')
    open_registration_from_lte = filters.IsoDateTimeFilter(
        field_name="open_registration_from", lookup_expr='lte')
    close_registration_at_gte = filters.IsoDateTimeFilter(
        field_name="close_registration_at", lookup_expr='gte')
    close_registration_at_lte = filters.IsoDateTimeFilter(
        field_name="close_registration_at", lookup_expr='lte')

    class Meta:
        model = Event
        exclude = ('headline_image', 'gpx_file', 'header_route_image', 'logo',
                   'accepted_indexes')


class EventAPI(DefaultViewSet):
    serializer_class = EventSerializer
    search_fields = ["name", 'general_area', 'course_profile']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    queryset = Event.objects.filter().order_by('-id')
    filterset_class = CustomFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedEventSerializer
        return super().get_serializer_class()


class AddonAPI(DefaultViewSet):
    serializer_class = AddonSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Addon.objects.filter().order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        slug = self.kwargs.get('active_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(event__slug=slug)


class MediaForAddonAPI(DefaultViewSet):
    serializer_class = MediaForAddonSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = MediaForAddon.objects.filter().order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        id = self.kwargs.get('addon_pk', None)
        if id is None:
            return self.queryset.none()
        return self.queryset.filter(addon__id=id)


class FAQAPI(DefaultViewSet):
    serializer_class = FAQSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = FAQ.objects.filter().order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        slug = self.kwargs.get('active_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(event__slug=slug)


class CategoryAPI(DefaultViewSet):
    serializer_class = CategorySerializer
    search_fields = ["name"]
    lookup_field = 'uuid'
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.filter().order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        slug = self.kwargs.get('active_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(event__slug=slug)


class PrizeAPI(DefaultViewSet):
    serializer_class = PrizeSerializer
    search_fields = ["rank", 'prize']
    permission_classes = [IsAdminOrReadOnly]
    queryset = Prize.objects.filter().order_by('-id').order_by(
        '-rank', '-gender')
    pagination_class = InfinitePagination

    def get_queryset(self):
        uuid = self.kwargs.get('category_uuid', None)
        if uuid is None:
            return self.queryset.none()
        return self.queryset.filter(category__uuid=uuid)


class ScheduleAPI(DefaultViewSet):
    serializer_class = ScheduleSerializer
    search_fields = ["id"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Schedule.objects.filter().order_by('-id').order_by('date')
    pagination_class = InfinitePagination

    def get_queryset(self):
        event_slug = self.kwargs.get('active_slug', None)
        if event_slug is None:
            return self.queryset.none()
        return self.queryset.filter(event__slug=event_slug)


class MediaAPI(DefaultViewSet):
    serializer_class = MediaForEventSerializer
    search_fields = ["id"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = MediaForEvent.objects.filter().order_by('-id').order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        event_slug = self.kwargs.get('active_slug', None)
        if event_slug is None:
            return self.queryset.none()
        return self.queryset.filter(event__slug=event_slug)


class MediaForCategoryAPI(DefaultViewSet):
    serializer_class = MediaForCategorySerializer
    search_fields = ["id"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = MediaForCategory.objects.filter().order_by('-id').order_by(
        '-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        uuid = self.kwargs.get('category_uuid', None)
        if uuid is None:
            return self.queryset.none()
        return self.queryset.filter(category__uuid=uuid)


class ResultListAPI(DefaultViewSet):
    serializer_class = ResultListSerializer
    search_fields = ["gender", 'description']
    permission_classes = [IsAdminOrReadOnly]
    queryset = ResultList.objects.filter().order_by('-id').order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        uuid = self.kwargs.get('category_uuid', None)
        if uuid is None:
            return self.queryset.none()
        return self.queryset.filter(category__uuid=uuid)


class ResultEntryAPI(DefaultViewSet):
    serializer_class = ResultEntrySerializer
    search_fields = [
        "full_name", 'gender', 'nationality', 'bib_number', 'itra_id'
    ]
    permission_classes = [IsAdminOrReadOnly]
    queryset = ResultEntry.objects.filter().order_by('-id').order_by(
        '-interval_unix_time')
    pagination_class = InfinitePagination

    def get_queryset(self):
        uuid = self.kwargs.get('category_uuid', None)
        if uuid is None:
            return self.queryset.none()
        return self.queryset.filter(result_list__category__uuid=uuid)

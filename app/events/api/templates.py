from core.utils.functions import InfinitePagination
from core.utils.viewsets import DefaultViewSet
from events.models import (AddonTemplate, CategoryTemplate, EventTemplate,
                           FAQTemplate, PrizeTemplate)
from events.models.event_templates import (MediaForCategoryTemplate,
                                           MediaForEventTemplate,
                                           MediaForAddonTemplate,
                                           ScheduleTemplate)
from events.utils import start_event_from_template
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .serializers.event import DetailedEventSerializer
from .serializers.event_templates import (
    AddonTemplateSerializer, CategoryTemplateSerializer,
    DetailedEventTemplateSerializer, EventTemplateSerializer,
    FAQTemplateSerializer, MediaForAddonTemplateSerializer,
    MediaForCategoryTemplateSerializer, MediaForEventTemplateSerializer,
    PrizeTemplateSerializer, ScheduleTemplateSerializer)


class EventTemplateAPI(DefaultViewSet):
    serializer_class = EventTemplateSerializer
    search_fields = ["name", 'general_area', 'course_profile']
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
    queryset = EventTemplate.objects.filter().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedEventTemplateSerializer
        return super().get_serializer_class()

    @action(methods=['post'], detail=True)
    def start(self, request, *args, **kwargs):
        event_template = self.get_object()
        event = start_event_from_template(event_template, request.data)
        return Response(DetailedEventSerializer(event).data,
                        status=status.HTTP_200_OK)


class AddonTemplateAPI(DefaultViewSet):
    serializer_class = AddonTemplateSerializer

    search_fields = ["name"]
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    queryset = AddonTemplate.objects.filter().order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        slug = self.kwargs.get('template_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(event_template__slug=slug)


class MediaForAddonTemplateAPI(DefaultViewSet):
    serializer_class = MediaForAddonTemplateSerializer
    search_fields = ["id"]
    permission_classes = [IsAdminUser]
    queryset = MediaForAddonTemplate.objects.filter().order_by('-id').order_by(
        '-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        id = self.kwargs.get('addon_id', None)
        if id is None:
            return self.queryset.none()
        return self.queryset.filter(addon_template__id=id)


class FAQTemplateAPI(DefaultViewSet):
    serializer_class = FAQTemplateSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminUser]
    queryset = FAQTemplate.objects.filter().order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        slug = self.kwargs.get('template_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(event_template__slug=slug)


class CategoryTemplateAPI(DefaultViewSet):
    serializer_class = CategoryTemplateSerializer
    search_fields = ["name"]
    lookup_field = 'uuid'
    permission_classes = [IsAdminUser]
    queryset = CategoryTemplate.objects.filter().order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        slug = self.kwargs.get('template_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(event_template__slug=slug)


class MediaForCategoryTemplateAPI(DefaultViewSet):
    serializer_class = MediaForCategoryTemplateSerializer
    search_fields = ["id"]
    permission_classes = [IsAdminUser]
    queryset = MediaForCategoryTemplate.objects.filter().order_by(
        '-id').order_by('-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        uuid = self.kwargs.get('category_uuid', None)
        if uuid is None:
            return self.queryset.none()
        return self.queryset.filter(category_template__uuid=uuid)


class PrizeTemplateAPI(DefaultViewSet):
    serializer_class = PrizeTemplateSerializer
    search_fields = ["rank", 'prize']
    permission_classes = [IsAdminUser]
    queryset = PrizeTemplate.objects.filter().order_by('-id').order_by(
        '-rank', '-gender')
    pagination_class = InfinitePagination

    def get_queryset(self):
        uuid = self.kwargs.get('category_uuid', None)
        if uuid is None:
            return self.queryset.none()
        return self.queryset.filter(category_template__uuid=uuid)


class MediaTemplateAPI(DefaultViewSet):
    serializer_class = MediaForEventTemplateSerializer
    search_fields = ["id"]
    permission_classes = [IsAdminUser]
    queryset = MediaForEventTemplate.objects.filter().order_by('-id').order_by(
        '-id')
    pagination_class = InfinitePagination

    def get_queryset(self):
        slug = self.kwargs.get('template_slug', None)
        if slug is None:
            return self.queryset.none()
        return self.queryset.filter(event_template__slug=slug)


class ScheduleTemplateAPI(DefaultViewSet):
    serializer_class = ScheduleTemplateSerializer
    search_fields = ["id"]
    permission_classes = [IsAdminUser]
    queryset = ScheduleTemplate.objects.filter().order_by('-id').order_by(
        'date')
    pagination_class = InfinitePagination

    def get_queryset(self):
        event_slug = self.kwargs.get('template_slug', None)
        if event_slug is None:
            return self.queryset.none()
        return self.queryset.filter(event_template__slug=event_slug)

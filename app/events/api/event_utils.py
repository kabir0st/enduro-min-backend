from core.utils.permissions import IsStaffOrReadOnly
from core.utils.viewsets import DefaultViewSet
from events.models import EventTag, EventType
from .serializers.event_utils import EventTagSerializer, EventTypeSerializer


class EventTypeAPI(DefaultViewSet):
    serializer_class = EventTypeSerializer
    search_fields = ["name"]
    lookup_field = 'slug'
    permission_classes = [IsStaffOrReadOnly]
    queryset = EventType.objects.filter().order_by('-id')


class EventTagAPI(DefaultViewSet):
    serializer_class = EventTagSerializer
    search_fields = ["name"]
    lookup_field = 'slug'
    permission_classes = [IsStaffOrReadOnly]
    queryset = EventTag.objects.filter().order_by('-id')

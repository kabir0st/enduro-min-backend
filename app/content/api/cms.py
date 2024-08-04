from content.api.serializers.cms import (HighLightEventsSerializer,
                                         HomePageLogoSerializer,
                                         TeamMemberSerializer,
                                         TestimonialSerializer)
from content.models.cms import (HighLightEvents, HomePageLogo, TeamMember,
                                Testimonial)
from core.permissions import IsAdminOrReadOnly
from core.utils.viewsets import DefaultViewSet, SingletonViewSet


class TestimonialAPI(DefaultViewSet):
    serializer_class = TestimonialSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Testimonial.objects.filter().order_by('-id')


class HomePageLogoAPI(DefaultViewSet):
    serializer_class = HomePageLogoSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = HomePageLogo.objects.filter().order_by('-id')


class HighLightEventsAPI(SingletonViewSet):
    serializer_class = HighLightEventsSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = HighLightEvents.objects.filter().order_by('-id')


class TeamMemberAPI(DefaultViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = TeamMember.objects.filter().order_by('-id')

from content.api.blog import BlogAPI, TagAPI
from content.api.cms import (HighLightEventsAPI, HomePageLogoAPI,
                             TeamMemberAPI, TestimonialAPI)
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('testimonials', TestimonialAPI)
router.register('logos', HomePageLogoAPI)
router.register('highlight-events', HighLightEventsAPI)
router.register('tags', TagAPI)
router.register('blogs', BlogAPI)
router.register('team-members', TeamMemberAPI)

urlpatterns = [
    path('', include(router.urls)),
]

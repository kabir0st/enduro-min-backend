from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from .api.event_utils import EventTagAPI, EventTypeAPI
from .api.events import (FAQAPI, AddonAPI, CategoryAPI, EventAPI, MediaAPI,
                         MediaForAddonAPI, MediaForCategoryAPI, PrizeAPI,
                         ResultEntryAPI, ResultListAPI, ScheduleAPI)
from .api.templates import (AddonTemplateAPI, CategoryTemplateAPI,
                            EventTemplateAPI, FAQTemplateAPI,
                            MediaForAddonTemplateAPI,
                            MediaForCategoryTemplateAPI, MediaTemplateAPI,
                            PrizeTemplateAPI, ScheduleTemplateAPI)

router = SimpleRouter()
router.register('tags', EventTagAPI)
router.register('types', EventTypeAPI)
router.register('active', EventAPI)
router.register('templates', EventTemplateAPI)

# Templates routes
template_router = routers.NestedSimpleRouter(router,
                                             r'templates',
                                             lookup='template')
template_router.register('addons', AddonTemplateAPI)
template_addon_router = routers.NestedSimpleRouter(template_router,
                                                   r'addons',
                                                   lookup='addon')
template_addon_router.register('medias', MediaForAddonTemplateAPI)

template_router.register('categories', CategoryTemplateAPI)

template_category_router = routers.NestedSimpleRouter(template_router,
                                                      r'categories',
                                                      lookup='category')
template_category_router.register('prizes', PrizeTemplateAPI)
template_category_router.register('medias', MediaForCategoryTemplateAPI)

template_router.register('faqs', FAQTemplateAPI)
template_router.register('medias', MediaTemplateAPI)
template_router.register('schedules', ScheduleTemplateAPI)

# Active Event routes
event_router = routers.NestedSimpleRouter(router, r'active', lookup='active')
event_router.register('addons', AddonAPI)
event_router_addons = routers.NestedSimpleRouter(event_router,
                                                 r'addons',
                                                 lookup='addon')
event_router_addons.register('medias', MediaForAddonAPI)
event_router.register('categories', CategoryAPI)
event_router.register('faqs', FAQAPI)
event_router.register('medias', MediaAPI)

event_router.register('schedules', ScheduleAPI)
event_category_router = routers.NestedSimpleRouter(event_router,
                                                   r'categories',
                                                   lookup='category')
event_category_router.register('prizes', PrizeAPI)
event_category_router.register('results', ResultListAPI)
event_category_router.register('results-entries', ResultEntryAPI)
event_category_router.register('medias', MediaForCategoryAPI)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(template_router.urls)),
    path('', include(template_addon_router.urls)),
    path('', include(template_category_router.urls)),
    path('', include(event_router.urls)),
    path('', include(event_router_addons.urls)),
    path('', include(event_category_router.urls)),
]

from content.models import (Blog, HighLightEvents, HomePageLogo, Testimonial,
                            TeamMember)
from content.models.blogs import Tag
from django.contrib import admin

admin.site.register(TeamMember)
admin.site.register(Blog)
admin.site.register(Testimonial)
admin.site.register(HomePageLogo)
admin.site.register(HighLightEvents)
admin.site.register(Tag)

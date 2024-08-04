from django.contrib import admin

from .models import (FAQ, Addon, AddonTemplate, Category, CategoryTemplate,
                     Event, EventTag, EventTemplate, EventType, FAQTemplate,
                     MediaForEvent, MediaForEventTemplate, Prize, ResultList,
                     ResultEntry, PrizeTemplate, Schedule, MediaForAddon,
                     MediaForAddonTemplate, MediaForCategory, ScheduleTemplate,
                     MediaForCategoryTemplate)

admin.site.register(EventType)
admin.site.register(EventTag)
admin.site.register(EventTemplate)
admin.site.register(AddonTemplate)
admin.site.register(FAQTemplate)
admin.site.register(CategoryTemplate)
admin.site.register(PrizeTemplate)
admin.site.register(Event)
admin.site.register(Addon)
admin.site.register(Category)
admin.site.register(Prize)
admin.site.register(FAQ)
admin.site.register(Schedule)

admin.site.register(MediaForEvent)
admin.site.register(MediaForEventTemplate)
admin.site.register(ResultList)
admin.site.register(ResultEntry)

admin.site.register(MediaForAddon)
admin.site.register(MediaForAddonTemplate)
admin.site.register(MediaForCategory)
admin.site.register(MediaForCategoryTemplate)
admin.site.register(ScheduleTemplate)

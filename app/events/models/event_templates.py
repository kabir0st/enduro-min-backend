from django.db import models

from .event_utils import EventTag, EventType
from .reference_models import (AddOnReferenceClass, CategoryReferenceClass,
                               EventReferenceClass, FAQReferenceClass,
                               PrizeReferenceClass, ReferenceMediaForEvent,
                               ScheduleReferenceClass)


class EventTemplate(EventReferenceClass):
    event_tags = models.ManyToManyField(EventTag,
                                        related_name='event_templates')
    event_type = models.ForeignKey(EventType,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='event_templates')


class MediaForEventTemplate(ReferenceMediaForEvent):
    event_template = models.ForeignKey(EventTemplate,
                                       on_delete=models.CASCADE,
                                       related_name='template_medias')


class AddonTemplate(AddOnReferenceClass):
    event_template = models.ForeignKey(EventTemplate,
                                       on_delete=models.CASCADE,
                                       related_name='template_addons')


class MediaForAddonTemplate(ReferenceMediaForEvent):
    addon_template = models.ForeignKey(AddonTemplate,
                                       on_delete=models.CASCADE,
                                       related_name='template_addons_medias')


class FAQTemplate(FAQReferenceClass):
    event_template = models.ForeignKey(EventTemplate,
                                       on_delete=models.CASCADE,
                                       related_name='template_faqs')


class CategoryTemplate(CategoryReferenceClass):
    event_template = models.ForeignKey(EventTemplate,
                                       on_delete=models.CASCADE,
                                       related_name='template_categories')


class MediaForCategoryTemplate(ReferenceMediaForEvent):
    category_template = models.ForeignKey(
        CategoryTemplate,
        on_delete=models.CASCADE,
        related_name='template_category_medias')


class PrizeTemplate(PrizeReferenceClass):
    category_template = models.ForeignKey(CategoryTemplate,
                                          on_delete=models.CASCADE,
                                          related_name='template_prizes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category_template', 'rank', 'gender'],
                name='rank template prize constraint')
        ]

    def __str__(self):
        return f'{self.category_template} {self.rank}'


class ScheduleTemplate(ScheduleReferenceClass):
    event_template = models.ForeignKey(EventTemplate,
                                       on_delete=models.CASCADE,
                                       related_name='template_schedules')

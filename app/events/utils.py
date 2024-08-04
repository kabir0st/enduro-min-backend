from core.utils.functions import copy_model, str_to_datetime
from django.db.transaction import atomic
from events.models import (Addon, AddOnReferenceClass, Category,
                           CategoryReferenceClass, Event, EventReferenceClass,
                           Prize, PrizeReferenceClass)
from rest_framework.exceptions import APIException

from events.models.event import (FAQ, MediaForAddon, MediaForCategory,
                                 MediaForEvent, Schedule)
from events.models.reference_models import (FAQReferenceClass,
                                            ReferenceMediaForCategory,
                                            ReferenceMediaForEvent,
                                            ReferenceMediaForAddons,
                                            ScheduleReferenceClass)


def start_event_from_template(event_template, data):
    start_datetime = str_to_datetime(data["start_datetime"])
    end_datetime = str_to_datetime(data["end_datetime"])
    if start_datetime > end_datetime:
        raise APIException(
            f'Event cannot start at {start_datetime} and end at {end_datetime}'
        )
    with atomic():
        event_obj = copy_model(event_template, Event, EventReferenceClass)
        event_obj.name = data['name']
        event_obj.from_template = event_template
        event_obj.start_datetime = start_datetime
        event_obj.end_datetime = end_datetime
        event_obj.event_type = event_template.event_type
        event_obj.open_registration_from = str_to_datetime(
            data['open_registration_from'])
        event_obj.close_registration_at = str_to_datetime(
            data['close_registration_at'])
        event_obj.save()
        event_obj.event_tags.set([
            tag.id for tag in event_template.event_tags.filter(is_active=True)
        ])
        event_obj.save()

        for addon_template in event_template.template_addons.filter(
                is_active=True):
            addon = copy_model(addon_template, Addon, AddOnReferenceClass)
            addon.event = event_obj
            addon.save()
            for media in addon_template.template_addons_medias.filter(
            ).order_by('-id'):
                addon_media = copy_model(media, MediaForAddon,
                                         ReferenceMediaForAddons)
                addon_media.addon = addon
                addon_media.save()
        for media in event_template.template_medias.filter().order_by('-id'):
            addon = copy_model(media, MediaForEvent, ReferenceMediaForEvent)
            addon.event = event_obj
            addon.save()
        for faq_template in event_template.template_faqs.filter(
                is_active=True):
            faq = copy_model(faq_template, FAQ, FAQReferenceClass)
            faq.event = event_obj
            faq.save()
        for schedule_template in event_template.template_schedules.filter(
                is_active=True):
            schedule = copy_model(schedule_template, Schedule,
                                  ScheduleReferenceClass)
            schedule.event = event_obj
            schedule.save()
        for category_template in event_template.template_categories.filter(
                is_active=True):
            category = copy_model(category_template, Category,
                                  CategoryReferenceClass)
            category.event = event_obj
            category.save()

            for prize_template in category_template.template_prizes.filter(
                    is_active=True):
                prize = copy_model(prize_template, Prize, PrizeReferenceClass)
                prize.category = category
                prize.save()

            for m in category_template.template_category_medias.filter(
            ).order_by('-id'):
                media = copy_model(m, MediaForCategory,
                                   ReferenceMediaForCategory)
                media.category = category
                media.save()
    return event_obj

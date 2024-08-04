from core.utils.models import TimeStampedModel
from django.db import models
from django.utils.timezone import now
from users.models.users import UserBase

from .event_templates import EventTemplate
from .event_utils import EventTag, EventType
from .reference_models import (AddOnReferenceClass, CategoryReferenceClass,
                               EventReferenceClass, FAQReferenceClass,
                               PrizeReferenceClass, ReferenceMediaForAddons,
                               ReferenceMediaForCategory,
                               ReferenceMediaForEvent, ScheduleReferenceClass)


class Event(EventReferenceClass):
    event_tags = models.ManyToManyField(EventTag, related_name='events')
    event_type = models.ForeignKey(EventType,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='events')
    from_template = models.ForeignKey(EventTemplate,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      related_name='events')

    start_datetime = models.DateTimeField(default=now)
    end_datetime = models.DateTimeField(default=now)
    open_registration_from = models.DateTimeField(default=now)
    close_registration_at = models.DateTimeField(default=now)

    close_registration_forcefully = models.BooleanField(default=False)

    @property
    def is_registration_open(self):
        return (
            self.open_registration_from < now() < self.close_registration_at
            and not self.close_registration_forcefully)


class MediaForEvent(ReferenceMediaForEvent):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='medias')


class Addon(AddOnReferenceClass):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='addons')


class MediaForAddon(ReferenceMediaForAddons):
    addon = models.ForeignKey(Addon,
                              on_delete=models.CASCADE,
                              related_name='medias')


class Category(CategoryReferenceClass):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='categories')

    @property
    def remaining_tickets(self):
        if self.is_ticket_limited:
            return self.ticket_limit - self.tickets.filter(
                is_paid=True, is_active=True).count()
        return True


class MediaForCategory(ReferenceMediaForCategory):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='medias')


class Prize(PrizeReferenceClass):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='prizes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'rank', 'gender'],
                                    name='rank prize constraint')
        ]

    def __str__(self):
        return f'{self.category} {self.rank}'


class FAQ(FAQReferenceClass):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='faqs')


def default_array():
    return []


class Schedule(ScheduleReferenceClass):
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name='schedules')


class ResultList(TimeStampedModel):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='results')
    description = models.TextField(null=True, blank=True)
    GENDER_CHOICE = [('male', "Male"), ('female', "Female"), ('open', "Open")]
    gender = models.CharField(max_length=6,
                              choices=GENDER_CHOICE,
                              default='open')


class ResultEntry(models.Model):
    result_list = models.ForeignKey(ResultList,
                                    on_delete=models.CASCADE,
                                    related_name='entries')
    linked_user = models.ForeignKey(UserBase,
                                    on_delete=models.CASCADE,
                                    related_name='result_entries',
                                    null=True,
                                    blank=True)
    full_name = models.CharField(max_length=255)
    GENDER_CHOICE = [('male', "Male"), ('female', "Female"), ('open', "Open")]
    gender = models.CharField(max_length=6,
                              choices=GENDER_CHOICE,
                              default='open')
    dob = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    itra_id = models.CharField(max_length=255, blank=True, null=True)
    bib_number = models.CharField(max_length=255, null=True, blank=True)
    team = models.CharField(max_length=255, null=True, blank=True)

    interval_unix_time = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.full_name}"

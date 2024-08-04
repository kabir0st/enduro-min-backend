from core.utils.models import SingletonModel, TimeStampedModel
from django.db import models
from events.models.event import Event


class Testimonial(TimeStampedModel):
    logo = models.ImageField(upload_to='cms/testimonial/',
                             null=True,
                             blank=True)
    name = models.CharField(max_length=255, default='')
    content = models.TextField()
    designation = models.CharField(max_length=255, blank=True, default='')
    company = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.name}"


class HomePageLogo(TimeStampedModel):
    logo = models.ImageField(upload_to='cms/logos/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)


class HighLightEvents(SingletonModel):
    main_event = models.ForeignKey(Event,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   related_name='main_event')
    carousel_events = models.ManyToManyField(Event, blank=True)


class TeamMember(TimeStampedModel):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    photo = models.ImageField(upload_to='cms/teams/', null=True, blank=True)
    website = models.URLField(default='')
    social_media = models.URLField(default='')

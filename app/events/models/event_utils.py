from core.utils.models import TimeStampedModel
from django.db import models


class EventType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)

    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.name}'


class EventTag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)

    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.name}'

import os
import random
from uuid import uuid4

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()
from functools import reduce

import django.apps
from django.contrib.auth import get_user_model
from django.db import models
from events.models import (AddonTemplate, CategoryTemplate, EventTag,
                           EventTemplate, EventType, FAQTemplate,
                           PrizeTemplate)
from faker import Faker

User = get_user_model()

admin = User.objects.create_superuser('admin@admin.com', 'Hero Staff', 'pass')
admin.save()

NO_CREATE = ['id', 'created_at', 'updated_at', 'slug', 'reverse_related']
NO_CREATE_TYPE = [
    models.ManyToOneRel, models.BigAutoField, models.ManyToManyField,
    models.ForeignKey, models.FileField, models.ImageField
]
NO_CREATE_TYPE_STR = ['reverse', 'related', 'Rel']

fake = Faker()

TEMPLATE_DEP = [AddonTemplate, FAQTemplate]


def get_factory_value(field_type):
    if field_type == models.CharField:
        return fake.name()
    if field_type == models.DateTimeField:
        return fake.future_datetime()
    if field_type == models.TextField:
        fake.paragraph(nb_sentences=5)
    if field_type == models.BooleanField:
        return True
    return fake.random_digit_not_null()


def field_validation_for_auto_fill(field):
    if field.name not in NO_CREATE:
        if type(field) not in NO_CREATE_TYPE:
            if not reduce(
                (lambda old_value, new_value: old_value * new_value),
                [word in str(type(field)) for word in NO_CREATE_TYPE_STR]):
                return True
    return False


def obj_factory(model, save=None):
    _obj = model()
    for field in model._meta.get_fields():
        if field_validation_for_auto_fill(field):
            value = get_factory_value(type(field))
            setattr(_obj, field.name, value)
    if save:
        _obj.save()
    return _obj


if __name__ == "__main__":
    tags = [obj_factory(EventTag, True) for _ in range(0, 9)]
    types = [obj_factory(EventType, True) for _ in range(0, 9)]
    for _ in range(0, 50):
        event = obj_factory(EventTemplate)
        event.event_type = types[random.randint(0, 8)]
        event.save()
        for _ in range(0, random.randint(0, 18)):
            event.event_tags.add(tags[random.randint(0, 8)])
        event.save()
        for dependent in TEMPLATE_DEP:
            for _ in range(0, random.randint(0, 4)):
                obj = obj_factory(dependent)
                obj.event_template = event
                obj.save()

        for _ in range(0, random.randint(0, 4)):
            obj = obj_factory(CategoryTemplate)
            obj.uuid = uuid4()
            obj.event_template = event
            obj.save()
            for i in range(0, 3):
                for gender in ['male', 'female']:
                    PrizeTemplate.objects.create(category_template=obj,
                                                 gender=gender,
                                                 rank=i,
                                                 prize=5000 * i)

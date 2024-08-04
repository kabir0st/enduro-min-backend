from core.utils.models import TimeStampedModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import UserBase

from .event import Event


class Review(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    review = models.TextField(default='')
    rate = models.PositiveBigIntegerField(
        default=5, validators=[MaxValueValidator(5),
                               MinValueValidator(0)])

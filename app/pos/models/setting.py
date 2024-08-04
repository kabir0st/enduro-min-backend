from core.utils.models import SingletonModel
from django.db import models


class Settings(SingletonModel):
    enable_payment = models.BooleanField(default=True)

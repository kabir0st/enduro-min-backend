from core.utils.functions import default_array
from core.utils.models import SingletonModel
from django.db import models


class Settings(SingletonModel):
    accepted_indexes = models.JSONField(default=default_array)
    usd_npr_exchange_rate = models.DecimalField(default=135.00,
                                                max_digits=60,
                                                decimal_places=2)

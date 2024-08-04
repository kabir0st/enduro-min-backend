from uuid import uuid4

from ckeditor.fields import RichTextField
from core.utils.functions import generate_upload_location
from core.utils.models import TimeStampedModel, validate_image_size
from django.db import models
from django.core.validators import FileExtensionValidator
from core.utils.functions import default_array


class EventReferenceClass(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    description = RichTextField(default='')
    general_area = models.TextField(default='')
    starts_from_location = models.TextField(default='')
    ends_at_location = models.TextField(default='')

    course_profile = models.CharField(max_length=255)

    things_required_to_bring = RichTextField(default='')
    things_recommended_to_bring = RichTextField(default='')

    legal_fine_print = RichTextField(default='')

    headline_image = models.FileField(upload_to=generate_upload_location,
                                      validators=[
                                          validate_image_size,
                                          FileExtensionValidator(
                                              ['jpg', 'jpeg', 'png', 'gif'])
                                      ],
                                      blank=True,
                                      null=True)
    header_route_image = models.FileField(
        upload_to=generate_upload_location,
        validators=[
            validate_image_size,
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])
        ],
        blank=True,
        null=True,
    )
    logo = models.FileField(
        upload_to=generate_upload_location,
        validators=[
            validate_image_size,
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])
        ],
        blank=True,
        null=True,
    )
    gpx_file = models.FileField(null=True,
                                blank=True,
                                upload_to=generate_upload_location)
    prize_description = RichTextField(null=True, blank=True)

    accepted_indexes = models.JSONField(default=default_array)

    def __str__(self):
        return f'{self.name}'

    class Meta(TimeStampedModel.Meta):
        abstract = True


class ReferenceMediaForEvent(TimeStampedModel):
    src = models.FileField(upload_to=generate_upload_location,
                           validators=[
                               validate_image_size,
                               FileExtensionValidator(
                                   ['jpg', 'jpeg', 'png', 'gif'])
                           ])

    class Meta(TimeStampedModel.Meta):
        abstract = True


class AddOnCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class AddOnReferenceClass(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = RichTextField(default='')
    addon_category = models.ForeignKey(AddOnCategory,
                                       on_delete=models.PROTECT,
                                       null=True,
                                       blank=True)

    nepali_price = models.DecimalField(default=0.0,
                                       max_digits=60,
                                       decimal_places=2)
    saarc_price = models.DecimalField(default=0.0,
                                      max_digits=60,
                                      decimal_places=2)
    international_price = models.DecimalField(default=0.0,
                                              max_digits=60,
                                              decimal_places=2)

    is_included_by_default = models.BooleanField(default=False)
    is_package = models.BooleanField(default=False)
    can_ignore_category_price = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta(TimeStampedModel.Meta):
        abstract = True


class ReferenceMediaForAddons(TimeStampedModel):
    src = models.FileField(upload_to=generate_upload_location,
                           validators=[
                               validate_image_size,
                               FileExtensionValidator(
                                   ['jpg', 'jpeg', 'png', 'gif'])
                           ])

    class Meta(TimeStampedModel.Meta):
        abstract = True


class FAQReferenceClass(TimeStampedModel):
    question = models.TextField(default='')
    answer = models.TextField(default='')

    def __str__(self):
        return f'{self.question}'

    class Meta(TimeStampedModel.Meta):
        abstract = True


class CategoryReferenceClass(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = RichTextField(default='', blank=True)
    extra_requirements = models.TextField(default='', blank=True)

    actual_distance = models.DecimalField(default=0.00,
                                          max_digits=60,
                                          decimal_places=2)
    elevation_gain = models.DecimalField(default=0.00,
                                         max_digits=60,
                                         decimal_places=2)
    elevation_lost = models.DecimalField(default=0.00,
                                         max_digits=60,
                                         decimal_places=2)
    highest_altitude = models.DecimalField(default=0.00,
                                           max_digits=60,
                                           decimal_places=2)
    number_of_checkpoints = models.PositiveBigIntegerField(default=0)
    cut_off_description = models.TextField(default='', blank=True)

    is_ticket_limited = models.BooleanField(default=False)
    ticket_limit = models.PositiveIntegerField(default=1)

    nepali_price = models.DecimalField(default=0.0,
                                       max_digits=60,
                                       decimal_places=2)
    saarc_price = models.DecimalField(default=0.0,
                                      max_digits=60,
                                      decimal_places=2)
    international_price = models.DecimalField(default=0.0,
                                              max_digits=60,
                                              decimal_places=2)

    winning_conditions = RichTextField(default='', blank=True)

    bib_prefix = models.CharField(max_length=255, null=True, blank=True)
    headline_image = models.FileField(upload_to=generate_upload_location,
                                      validators=[
                                          validate_image_size,
                                          FileExtensionValidator(
                                              ['jpg', 'jpeg', 'png', 'gif'])
                                      ],
                                      blank=True,
                                      null=True)

    gpx_file = models.FileField(null=True,
                                blank=True,
                                upload_to=generate_upload_location)

    def __str__(self):
        return f'{self.name}'

    class Meta(TimeStampedModel.Meta):
        abstract = True


class ReferenceMediaForCategory(TimeStampedModel):
    src = models.FileField(upload_to=generate_upload_location,
                           validators=[
                               validate_image_size,
                               FileExtensionValidator(
                                   ['jpg', 'jpeg', 'png', 'gif'])
                           ])

    class Meta(TimeStampedModel.Meta):
        abstract = True


class PrizeReferenceClass(TimeStampedModel):
    GENDER_CHOICE = [('male', "Male"), ('female', "Female"), ('open', "Open")]
    gender = models.CharField(max_length=6,
                              choices=GENDER_CHOICE,
                              default='open')
    rank = models.PositiveIntegerField(default=1)
    prize = models.TextField(default='', blank=True)

    class Meta(TimeStampedModel.Meta):
        abstract = True


class ScheduleReferenceClass(TimeStampedModel):
    title = models.CharField(max_length=255, default='')
    description = RichTextField()

    schedule_json = models.JSONField(default=default_array)
    distance_covered = models.DecimalField(default=0.00,
                                           max_digits=60,
                                           decimal_places=2)
    elevation_gained = models.DecimalField(default=0.00,
                                           max_digits=60,
                                           decimal_places=2)
    elevation_lost = models.DecimalField(default=0.00,
                                         max_digits=60,
                                         decimal_places=2)
    maximum_elevation = models.DecimalField(default=0.00,
                                            max_digits=60,
                                            decimal_places=2)

    checkpoints = models.PositiveIntegerField(default=0)

    headline = models.FileField(upload_to=generate_upload_location, null=True)
    gpx_file = models.FileField(upload_to=generate_upload_location, null=True)

    date = models.DateField()

    class Meta(TimeStampedModel.Meta):
        abstract = True

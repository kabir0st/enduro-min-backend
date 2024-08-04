from ckeditor.fields import RichTextField
from core.utils.models import TimeStampedModel
from django.db import models
from django.utils.text import slugify
from users.models import UserBase


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255)


class Blog(TimeStampedModel):
    author = models.ForeignKey(UserBase, on_delete=models.CASCADE)

    author_name = models.CharField(max_length=255, null=True, blank=True)

    title = models.CharField(max_length=255, unique=True)
    sub_title = models.TextField(null=True, blank=True)

    content = RichTextField()
    minutes_to_read = models.PositiveBigIntegerField(default=5)

    cover_image = models.ImageField(null=True, blank=True, upload_to='blogs/')

    slug = models.SlugField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

import random
import uuid

from core.utils.models import TimeStampedModel
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils import timezone
from users.tasks import send_otp_email


class VerificationCode(models.Model):
    code = models.CharField(null=True,
                            blank=True,
                            max_length=6,
                            editable=False)
    email = models.EmailField()
    is_email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
    otp_for = models.CharField(max_length=255, default='email_verification')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'email'],
                                    name='verification_unique_constraints')
        ]

    def has_expire(self):
        return self.expiration_time and self.expiration_time < timezone.now()

    def check_code(self, code):
        if self.expiration_time and self.expiration_time < timezone.now():
            return False, 'Code has already expired.'
        if self.code == str(code):
            return True, None
        return False, 'Invalid verification code.'

    @classmethod
    def generate(cls, email, otp_for):
        old_codes = cls.objects.filter(email=email, otp_for=otp_for)
        if old_codes:
            for old_code in old_codes:
                if not old_code.has_expire():
                    raise ValidationError(
                        'Last verification code has not expired yet.')
                old_codes.delete()
        verification_code = cls(email=email, otp_for=otp_for)
        verification_code.expiration_time = timezone.now(
        ) + timezone.timedelta(minutes=5)
        verification_code.save()
        return verification_code


@receiver(pre_save, sender=VerificationCode)
def pre_save_verification_code(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = str(random.randint(111111, 999999))


@receiver(post_save, sender=VerificationCode)
def post_save_handler_verification_code(sender, instance, created, **kwargs):
    if not instance.is_email_sent:
        try:
            send_otp_email(instance.id)
        except Exception as e:
            print(e)


class Document(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='processing')
    document = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'{self.model}: {self.uuid}'

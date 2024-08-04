import uuid
from decimal import Decimal

from core.utils.functions import are_model_fields_equal, default_json
from core.utils.models import TimeStampedModel
from django.db import models
from django.dispatch import receiver
from events.models import Addon, Category
from events.models.event import default_array
from users.models import UserBase


class Ticket(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_by = models.ForeignKey(UserBase,
                                      on_delete=models.PROTECT,
                                      related_name='registered_tickets')
    user = models.ForeignKey(UserBase,
                             on_delete=models.PROTECT,
                             related_name='tickets')

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    addons = models.ManyToManyField(Addon, blank=True)
    price_applied = models.CharField(default='nepali', max_length=255)
    # {
    #     f'{addon_id}': quantity,
    #     f'{addon_id}': quantity,
    #     f'{addon_id}': quantity
    # }
    addon_quantity = models.JSONField(default=default_json,
                                      null=True,
                                      blank=True)

    # ticket profile
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=8, default='male')
    email = models.EmailField()
    dob = models.DateField()
    address = models.TextField(default='', blank=True)
    zip_code = models.CharField(max_length=10, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='nepal')
    phone_number = models.CharField(max_length=14, default='')
    organization = models.TextField(default='', blank=True)
    BLOOD_GROUPS = (('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                    ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
                    ('unknown', 'Unknown'))
    blood_group = models.CharField(max_length=7,
                                   choices=BLOOD_GROUPS,
                                   default='unknown')
    emergency_name = models.CharField(max_length=255, default='')
    emergency_contact = models.CharField(max_length=14, default='')
    relation = models.CharField(max_length=255, blank=True, default='')
    user_indexes = models.JSONField(default=default_array,
                                    null=True,
                                    blank=True)
    user_note = models.TextField(default='', null=True, blank=True)
    size_preference = models.CharField(max_length=255, default='medium')
    bib = models.CharField(max_length=255, blank=True, default='')

    # auto calculated fields
    base_ticket_amount = models.DecimalField(max_digits=10,
                                             decimal_places=2,
                                             default=0.00)
    total_addons_amount = models.DecimalField(max_digits=10,
                                              decimal_places=2,
                                              default=0.00)
    bill_amount = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      default=0.00)

    is_cancelled = models.BooleanField(default=False)
    cancel_remarks = models.CharField(max_length=255, default='', blank=True)
    is_refunded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.uuid}"


@receiver(models.signals.pre_save, sender=Ticket)
def handle_ticket_pre_save(sender, instance, *args, **kwargs):
    instance.price_applied = instance.price_applied.lower()
    if instance.id:
        if invoice := instance.invoice.filter().first():
            if invoice.is_paid:
                old = Ticket.objects.get(id=instance.id)
                if not are_model_fields_equal(old, instance, 'category',
                                              'addons', 'price_applied',
                                              'addon_quantity'):
                    raise Exception(
                        'Cannot Update category, addons or country (price '
                        'applied) after the invoice has been paid.')


@receiver(models.signals.post_save, sender=Ticket)
def handle_ticket_post_save(sender, instance, created, *args, **kwargs):

    instance.base_ticket_amount = getattr(instance.category,
                                          f'{instance.price_applied}_price')
    total_addon_price = Decimal('0.00')
    for addon in instance.addons.filter(is_active=True):
        total_addon_price = total_addon_price + getattr(
            addon, f'{instance.price_applied}_price'
        ) * instance.addon_quantity.get(str(addon.id), 0)

    fields_to_convert = ['base_ticket_amount', 'total_addons_amount']

    instance.total_addons_amount = total_addon_price

    for field in fields_to_convert:
        setattr(instance, field, Decimal(f'{getattr(instance, field)}'))

    instance.bill_amount = (instance.base_ticket_amount +
                            instance.total_addons_amount)

    models.signals.post_save.disconnect(handle_ticket_post_save, sender=Ticket)
    instance.save()
    if not created:
        [invoice.save() for invoice in instance.invoice.filter()]
    models.signals.post_save.connect(handle_ticket_post_save, sender=Ticket)


class InvoiceSummary(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserBase,
                             on_delete=models.PROTECT,
                             related_name='invoices')
    tickets = models.ManyToManyField(Ticket, related_name='invoice')

    paid_amount = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      default=0.00)

    total_bill_amount = models.DecimalField(max_digits=10,
                                            decimal_places=2,
                                            default=0.00)

    extra_charge = models.DecimalField(max_digits=10,
                                       decimal_places=2,
                                       default=0.00)
    extra_charge_remarks = models.CharField(max_length=255,
                                            blank=True,
                                            default='')

    discount_amount = models.DecimalField(max_digits=10,
                                          decimal_places=2,
                                          default=0.00)
    discount_remarks = models.CharField(max_length=255, blank=True, default='')
    tax_amount = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     default=0.00)
    tax_remarks = models.CharField(max_length=255, blank=True, default='')

    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.uuid}"

    def check_is_paid(self):
        return self.paid_amount >= self.total_bill_amount

    @property
    def invoice_number(self):
        return f"{self.id}-{str(self.uuid)[:4]}"


@receiver(models.signals.pre_save, sender=InvoiceSummary)
def handle_invoice_summary_pre_save(sender, instance, *args, **kwargs):
    instance.total_bill_amount = Decimal('0.00')
    instance.paid_amount = Decimal('0.00')

    fields_to_convert = ['extra_charge', 'tax_amount', 'discount_amount']
    for field in fields_to_convert:
        setattr(instance, field, Decimal(f'{getattr(instance, field)}'))
    if instance.id:
        for ticket in instance.tickets.filter(is_cancelled=False):
            instance.total_bill_amount = (instance.total_bill_amount +
                                          ticket.bill_amount)
            instance.total_bill_amount = (instance.total_bill_amount -
                                          instance.discount_amount +
                                          instance.extra_charge +
                                          instance.tax_amount +
                                          instance.tax_amount)
        for payment in instance.payments.filter(is_refunded=False):
            instance.paid_amount += payment.amount
    instance.is_paid = instance.check_is_paid()

import math
from decimal import Decimal

import stripe
from core.settings.environments import ENDPOINT_SECRET, STRIPE_PUBLISHABLE_KEY
from core.utils.viewsets import DefaultViewSet
from django.db import transaction
from django_filters import rest_framework as filters
from events.models.event import Category
from pos.api.serializers.payments import PaymentSerializer
from pos.models import Ticket
from pos.models.payment import FonePayPayment, Payment, StripePayment
from pos.models.ticket import InvoiceSummary
from pos.utils import generate_fonepay_qr, verify_qr
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models.settings import Settings

from .serializers.tickets import (InvoiceSummarySerializer,
                                  MiniInvoiceSummarySerializer,
                                  MiniTicketSerializer, TicketSerializer)


class TicketFilter(filters.FilterSet):
    is_paid = filters.BooleanFilter(label='is_paid', method='filter_is_paid')

    class Meta:
        model = Ticket
        exclude = ('addon_quantity', 'user_indexes')

    def filter_is_paid(self, queryset, name, value):
        return queryset.filter(invoice__is_paid=value)


class TicketAPI(DefaultViewSet):
    serializer_class = TicketSerializer
    search_fields = [
        'first_name', 'last_name', 'email', 'phone_number', 'uuid'
    ]
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.filter().order_by('-id')
    filterset_class = TicketFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return MiniTicketSerializer
        return self.serializer_class

    def get_queryset(self):
        event_slug = self.request.GET.get('event', None)
        if not self.request.user.is_staff:
            queryset = Ticket.objects.filter(user=self.request.user)
        else:
            queryset = super().get_queryset()
        if event_slug:
            queryset = queryset.filter(category__event__slug=event_slug)
        return queryset

    def handle_ticket_creation(self, request, data):
        data['registered_by'] = self.request.user.id
        if data.get('user', None) is not None:
            if not self.request.user.is_staff:
                data['user'] = self.request.user.id
        else:
            data['user'] = self.request.user.id
        data['category'] = Category.objects.get(uuid=data['category']).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        ticket.save()
        return ticket

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if not isinstance(data, list):
            data = [data]
        tickets = []
        user = None
        with transaction.atomic():
            for ticket in data:
                ticket = self.handle_ticket_creation(request, ticket)
                tickets.append(ticket.id)
                user = ticket.user
            summary = InvoiceSummary.objects.create(user=user)
            summary.tickets.set(tickets)
            summary.save()

        return Response(
            InvoiceSummarySerializer(summary).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['registered_by'] = self.request.user.id
        if not self.request.user.is_staff:
            data['user'] = self.request.user.id
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class InvoiceSummaryFilter(filters.FilterSet):
    event_str = filters.CharFilter(label='event', method='filter_event')

    class Meta:
        model = InvoiceSummary
        fields = '__all__'

    def filter_event(self, queryset, name, value):
        value = int(value)
        return queryset.filter(
            tickets__category__event__name__icontains=value).distinct('id')


class InvoiceSummaryAPI(DefaultViewSet):
    serializer_class = InvoiceSummarySerializer
    search_fields = [
        'uuid',
        'tickets__uuid',
        'user__email',
        'tickets__email',
    ]
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated]
    queryset = InvoiceSummary.objects.filter().order_by('-id')
    http_method_names = ['get', 'post']
    filterset_class = InvoiceSummaryFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return MiniInvoiceSummarySerializer
        return self.serializer_class

    def get_queryset(self):
        if not self.request.user.is_staff:
            return InvoiceSummary.objects.filter(
                tickets__user=self.request.user)
        return super().get_queryset()

    @action(methods=['POST', 'post'], detail=True)
    def staff_approved_payment(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise APIException('Only Staff can add staff approved payments.')
        summary = self.get_object()
        with transaction.atomic():
            Payment.objects.create(payment_type='staff_approved',
                                   amount=Decimal(f'{request.data["amount"]}'),
                                   invoice_summary=summary,
                                   remarks='Payment Through API')
            response = {
                'status': True,
                'data': InvoiceSummarySerializer(summary).data,
                'type': 'invoice-summary'
            }
        return Response(response, status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True)
    def initiate_stripe_payment(self, request, *args, **kwargs):
        invoice = self.get_object()
        settings = Settings.load()
        bill_amount = math.ceil(invoice.total_bill_amount * 100 /
                                settings.usd_npr_exchange_rate)
        if bill_amount < settings.usd_npr_exchange_rate:
            raise APIException(
                'Cannot use stripe to process amount less than 1$.')
        if invoice.user.stripe_customer_id:
            customer = stripe.Customer.retrieve(
                invoice.user.stripe_customer_id)
        else:
            customer = stripe.Customer.create(
                email=invoice.user.email,
                name=f"{invoice.user.first_name} {invoice.user.last_name}")
            invoice.user.stripe_customer_id = customer['id']
            invoice.user.save()
        ephemeralKey = stripe.EphemeralKey.create(
            customer=customer['id'],
            stripe_version='2023-08-16',
        )
        paymentIntent = stripe.PaymentIntent.create(
            amount=bill_amount,
            currency='usd',
            customer=customer['id'],
            statement_descriptor='HTR Event',
            metadata={"uuid": invoice.uuid})
        StripePayment.objects.create(reference_id=paymentIntent.id,
                                     amount=bill_amount,
                                     status='initialized')
        response = {
            'clientSecret': paymentIntent.client_secret,
            'ephemeralKey': ephemeralKey.secret,
            'customer': customer.id,
            'publishableKey': STRIPE_PUBLISHABLE_KEY,
            'bill_amount': bill_amount
        }
        return Response(response, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def initiate_fonepay(self, request, *args, **kwargs):
        obj = self.get_object()
        fonepay_obj = FonePayPayment.objects.create(
            amount=request.data['amount'], invoice_number=obj.invoice_number)
        res = generate_fonepay_qr(fonepay_obj)
        return Response(res)

    @action(methods=['post'], detail=True)
    def verify_fonepay(self, request, *args, **kwargs):
        obj = FonePayPayment.objects.get(id=request.data['fonepay_payment_id'])
        obj.qr_status = 'success'
        obj.save()
        if obj.is_verified_from_server:
            raise Exception('Cannot verify payments that is already verified')
        with transaction.atomic():
            res = verify_qr(obj)
            if res['status']:
                payment_data = {
                    'amount': obj.amount,
                    'fonepay_payment': obj.id,
                    'payment_type': 'fonepay',
                    'invoice_summary': self.get_object().id
                }
                serializer = PaymentSerializer(data=payment_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    'status': True,
                    'msg': 'Payment successful.',
                    'data-type': 'payment',
                    'data': serializer.data
                })
            return Response({
                'status': False,
                'msg': 'There was problem verifying your payment.',
                'exception': res['text']
            })


@api_view(['post'])
@permission_classes([AllowAny])
def stripe_call_back(request, *args, **kwargs):
    settings = Settings.load()
    if ENDPOINT_SECRET:
        sig_header = request.headers.get('Stripe-Signature')
        try:
            event = stripe.Webhook.construct_event(request.body, sig_header,
                                                   ENDPOINT_SECRET)
        except stripe.error.SignatureVerificationError:
            return Response({
                'success': False,
                'status': False,
                'msg': 'Invalid Signature.'
            })
    payment_intent = None
    if 'payment_intent' in event['type']:
        payment_intent = event['data']['object']
        stripe_payment = StripePayment.objects.get(
            reference_id=payment_intent['id'])
        new_status = event['type'].replace('payment_intent.', '')
        if stripe_payment.status != new_status:
            stripe_payment.status = new_status
            stripe_payment.save()
            if stripe_payment.status == 'succeeded':
                invoice = InvoiceSummary.objects.get(
                    uuid=payment_intent['metadata']['uuid'])
                a = settings.usd_npr_exchange_rate
                Payment.objects.create(
                    payment_type='stripe',
                    invoice_summary=invoice,
                    amount=Decimal(f'{a*payment_intent["amount"]/100}'),
                    stripe=stripe_payment)
    return Response({
        'success': True,
    })


@api_view(['get'])
@permission_classes([AllowAny])
def usd_to_nepali(request):
    settings = Settings.load()
    return Response({
        'status': True,
        'rate': settings.usd_npr_exchange_rate,
        'from': 'usd',
        'to': 'npr'
    })

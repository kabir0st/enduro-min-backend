from events.api.serializers.event import (AddonSerializer, CategorySerializer,
                                          EventSerializer)
from pos.api.serializers.payments import PaymentSerializer
from pos.models import Ticket
from pos.models.ticket import InvoiceSummary
from rest_framework import serializers
from users.api.serializers.userbase import UserBaseSerializer


class MiniTicketSerializer(serializers.ModelSerializer):
    user_details = UserBaseSerializer(source='user', read_only=True)
    event_str = serializers.SerializerMethodField(read_only=True)
    is_paid = serializers.SerializerMethodField(read_only=True)

    category_str = serializers.SerializerMethodField(read_only=True)
    invoice_uuid = serializers.SerializerMethodField(read_only=True)
    addon_info = serializers.SerializerMethodField(read_only=True)

    def get_addon_info(self, obj):
        data = {}
        for addon in obj.category.event.addons.filter():
            data[addon.name] = obj.addon_quantity.get(str(addon.id), 0)
        return data

    def get_invoice_uuid(self, obj):
        return f'{obj.invoice.all().first().uuid}'

    def get_category_str(self, obj):
        return f"{obj.category.name}"

    def get_event_str(self, obj):
        return f"{obj.category.event.name}"

    def get_is_paid(self, obj):
        return obj.invoice.all().first().is_paid

    class Meta:
        model = Ticket
        exclude = ('id', )
        read_only_fields = ('is_active', )


class TicketSerializer(serializers.ModelSerializer):
    user_details = UserBaseSerializer(source='user', read_only=True)
    event_details = serializers.SerializerMethodField(read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)
    addon_details = AddonSerializer(source='addons', read_only=True, many=True)
    invoice_uuid = serializers.SerializerMethodField(read_only=True)
    is_paid = serializers.SerializerMethodField(read_only=True)
    addon_info = serializers.SerializerMethodField(read_only=True)

    def get_addon_info(self, obj):
        data = {}
        for addon in obj.category.event.addons.filter():
            data[addon.name] = obj.addon_quantity.get(str(addon.id), 0)
        return data

    def get_event_details(self, obj):
        return EventSerializer(instance=obj.category.event).data

    def get_is_paid(self, obj):
        return obj.invoice.all().first().is_paid

    def get_invoice_uuid(self, obj):
        return f'{obj.invoice.all().first().uuid}'

    class Meta:
        model = Ticket
        exclude = ('id', )
        read_only_fields = ('is_active', )


class TicketListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        exclude = ('id', )


class MiniInvoiceSummarySerializer(serializers.ModelSerializer):
    user_details = UserBaseSerializer(source='user', read_only=True)
    is_paid = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    def get_created_at(self, obj):
        return f"{obj.created_at}"

    def get_is_paid(self, instance):
        return instance.is_paid

    class Meta:
        model = InvoiceSummary
        exclude = ('id', )


class InvoiceSummarySerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    user_details = UserBaseSerializer(source='user', read_only=True)
    is_paid = serializers.SerializerMethodField(read_only=True)

    payments = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    def get_created_at(self, obj):
        return f"{obj.created_at}"

    def get_payments(self, obj):
        return PaymentSerializer(instance=obj.payments.filter(is_active=True),
                                 many=True).data

    def get_is_paid(self, instance):
        return instance.is_paid

    class Meta:
        model = InvoiceSummary
        exclude = ('id', )

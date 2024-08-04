from pos.models import FonePayPayment, Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class FonePayPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FonePayPayment
        fields = '__all__'

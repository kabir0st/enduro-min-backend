from core.utils.viewsets import DefaultViewSet
from pos.models.payment import Payment
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers.payments import PaymentSerializer


class PaymentAPI(DefaultViewSet):
    serializer_class = PaymentSerializer
    search_fields = []
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.filter().order_by('-id')
    http_method_names = ('get')

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset(
            invoice_summary__user=self.request.user)

    @action(methods=['GET'], detail=True)
    def refund(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        obj = self.get_object()
        obj.is_refunded = True
        obj.refunded_remarks = request.GET.get('remarks', '')
        obj.save()
        obj.invoice_summary.save()
        return Response({'status': True}, status=status.HTTP_200_OK)

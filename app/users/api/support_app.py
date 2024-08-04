from core.utils.viewsets import DefaultViewSet
from users.api.serializers.support import (DocumentSerializer,
                                           VerificationCodeSerializer)
from core.permissions import IsAdmin
from users.models.supports import Document, VerificationCode


class DocumentAPI(DefaultViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.filter().order_by('-id')
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'delete']
    lookup_field = 'uuid'


class VerificationCodeAPI(DefaultViewSet):
    serializer_class = VerificationCodeSerializer
    queryset = VerificationCode.objects.filter().order_by('-id')
    permission_classes = [IsAdmin]
    http_method_names = ['get']

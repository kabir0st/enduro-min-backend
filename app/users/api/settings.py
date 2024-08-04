from core.utils.viewsets import SingletonViewSet
from users.api.serializers.settings import SettingsSerializer
from users.models.settings import Settings
from core.permissions import IsAdminOrReadOnly


class SettingsAPI(SingletonViewSet):
    serializer_class = SettingsSerializer
    queryset = Settings.objects.filter().order_by('-id')
    permission_classes = [IsAdminOrReadOnly]

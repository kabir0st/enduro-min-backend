from content.api.serializers.blogs import (BlogSerializer,
                                           DetailBlogSerializer, TagSerializer)
from content.models.blogs import Blog, Tag
from core.permissions import IsAdminOrReadOnly
from core.utils.viewsets import DefaultViewSet


class TagAPI(DefaultViewSet):
    serializer_class = TagSerializer
    search_fields = ["name"]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Tag.objects.filter().order_by('-id')


class BlogAPI(DefaultViewSet):
    serializer_class = DetailBlogSerializer
    search_fields = ['title', 'sub_title', 'author']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    queryset = Blog.objects.filter().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogSerializer
        return super().get_serializer_class()

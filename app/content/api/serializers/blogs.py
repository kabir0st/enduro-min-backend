from content.models import Blog
from content.models.blogs import Tag
from rest_framework.serializers import ModelSerializer
from core.utils.serializers import Base64ImageField
from users.api.serializers.userbase import UserBaseSerializer


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class BlogSerializer(ModelSerializer):
    tag_details = TagSerializer(many=True, source='tags', read_only=True)
    author_details = UserBaseSerializer(source='author', read_only=True)
    cover_image = Base64ImageField()

    class Meta:
        model = Blog
        exclude = ('content', )

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class DetailBlogSerializer(ModelSerializer):
    tag_details = TagSerializer(many=True, source='tags', read_only=True)
    author_details = UserBaseSerializer(source='author', read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'

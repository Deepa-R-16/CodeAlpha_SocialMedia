from rest_framework import serializers
from .models import Post, Like, Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'author', 'text', 'parent', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author      = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked    = serializers.SerializerMethodField()
    media_url   = serializers.SerializerMethodField()

    # This is the key fix — media_file must be here as write_only
    # so it gets saved when uploaded, but media_url is used for reading
    media_file  = serializers.FileField(write_only=True, required=False)

    class Meta:
        model  = Post
        fields = [
            'id', 'author', 'post_type', 'caption',
            'media_file',   # write only — receives the uploaded file
            'media_url',    # read only  — returns the full URL
            'likes_count', 'is_liked', 'created_at'
        ]

    def get_likes_count(self, obj):
        return obj.likes_count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False

    def get_media_url(self, obj):
        if not obj.media_file:
            return None
        request = self.context.get('request')
        try:
            url = obj.media_file.url
            if request and url.startswith('/'):
                return request.build_absolute_uri(url)
            return url
        except Exception:
            return None
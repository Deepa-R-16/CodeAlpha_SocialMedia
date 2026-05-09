from rest_framework import serializers
from .models import Story
from users.serializers import UserSerializer

class StorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    media_url = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'author', 'media_url', 'created_at', 'expires_at']

    def get_media_url(self, obj):
        if obj.media:
            return obj.media.url
        return None
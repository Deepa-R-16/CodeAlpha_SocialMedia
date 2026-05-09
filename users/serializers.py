from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Follow


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    avatar_url      = serializers.SerializerMethodField()

    class Meta:
        model  = Profile
        fields = ['bio', 'avatar_url', 'website', 'is_private',
                  'followers_count', 'following_count']

    def get_followers_count(self, obj): return obj.followers_count()
    def get_following_count(self, obj): return obj.following_count()

    def get_avatar_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request')
        url = obj.avatar.url
        if request:
            return request.build_absolute_uri(url)
        return url


class UserSerializer(serializers.ModelSerializer):
    profile  = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'password', 'profile']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        Profile.objects.create(user=user)
        return user
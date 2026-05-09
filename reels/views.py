from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from posts.serializers import PostSerializer

class ReelListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(post_type='reel')
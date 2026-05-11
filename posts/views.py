from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer


class FeedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        from users.models import Follow
        ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list('following_id', flat=True)
        return Post.objects.filter(author_id__in=ids)


class PostListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = PostSerializer
    queryset           = Post.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)

        # Return the full post with media_url included
        out = PostSerializer(post, context={'request': request})
        return Response(out.data, status=201)


class PostDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = PostSerializer
    queryset           = Post.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class UserPostsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Post.objects.filter(author_id=self.kwargs['user_id'])


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({'liked': False, 'count': post.likes_count()})
        return Response({'liked': True, 'count': post.likes_count()})


class CommentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['pk'], parent=None
        )

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)
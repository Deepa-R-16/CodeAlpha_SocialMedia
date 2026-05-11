from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Story
from .serializers import StorySerializer

class StoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StorySerializer

    def get_queryset(self):
        return Story.objects.filter(
            expires_at__gt=timezone.now()
        ).order_by('-created_at')

class StoryCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StorySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Story(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    media      = models.FileField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    views      = models.ManyToManyField(User, related_name='viewed_stories', blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
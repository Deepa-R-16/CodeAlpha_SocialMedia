from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    POST_TYPES = [('photo','Photo'),('video','Video'),('reel','Reel'),
                  ('long_video','Long Video'),('audio','Audio'),('note','Note')]

    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_type  = models.CharField(max_length=20, choices=POST_TYPES, default='photo')
    caption    = models.TextField(blank=True)
    media_file = models.FileField(upload_to='posts/', blank=True, null=True)
    thumbnail  = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def likes_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent     = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
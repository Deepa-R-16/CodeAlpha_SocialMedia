from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',          include('users.urls')),
    path('api/posts/',         include('posts.urls')),
    path('api/stories/',       include('stories.urls')),
    path('api/reels/',         include('reels.urls')),
    path('api/notifications/', include('notifications.urls')),
]

# This line makes Django serve uploaded files locally during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=getattr(settings, 'MEDIA_ROOT', '')
    )
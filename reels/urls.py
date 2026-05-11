from django.urls import path
from .views import ReelListView

urlpatterns = [
    path('', ReelListView.as_view()),
]
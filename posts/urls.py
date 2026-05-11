from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.PostListView.as_view()),
    path('feed/',                   views.FeedView.as_view()),
    path('create/',                 views.PostCreateView.as_view()),
    path('<int:pk>/',               views.PostDetailView.as_view()),
    path('<int:pk>/like/',          views.LikeView.as_view()),
    path('<int:pk>/comments/',      views.CommentView.as_view()),
    path('user/<int:user_id>/',     views.UserPostsView.as_view()),
]
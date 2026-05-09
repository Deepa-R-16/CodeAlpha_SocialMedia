from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/',                  views.RegisterView.as_view()),
    path('login/',                     views.LoginView.as_view()),
    path('token/refresh/',             TokenRefreshView.as_view()),
    path('me/',                        views.MeView.as_view()),
    path('profile/update/',            views.ProfileUpdateView.as_view()),
    path('follow/<int:user_id>/',      views.FollowView.as_view()),
    path('users/<int:user_id>/',       views.UserDetailView.as_view()),
    path('users/suggest/',             views.SuggestUsersView.as_view()),
    path('search/',                    views.SearchView.as_view()),
]
from django.urls import path
from .views import (
  UserListCreateView,
  UserDetailView,
  LoginView,
  TokenLoginView
)

urlpatterns = [
  path('api/users', UserListCreateView.as_view(), name='user-list-create'),
  path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
  path('sign-in', LoginView.as_view(), name='login'),
  path('sign-in-with-token', TokenLoginView.as_view(), name='token-login'),
]
from django.urls import path, re_path
from .views import (
  UserAPIView,
  LoginView,
  TokenLoginView
)

urlpatterns = [
  re_path(r'^api/users/?$', UserAPIView.as_view(), name='users'),
  re_path(r'^api/users/(?P<pk>\d+)/?$', UserAPIView.as_view(), name='user-detail'),
  path('sign-in', LoginView.as_view(), name='login'),
  path('sign-in-with-token', TokenLoginView.as_view(), name='token-login'),
]
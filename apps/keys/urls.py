from django.urls import re_path
from .views import KeyAPIView

urlpatterns = [
  re_path(r'^keys/?$', KeyAPIView.as_view(), name='keys'),
  re_path(r'^keys/(?P<pk>\d+)/?$', KeyAPIView.as_view(), name='key-detail'),
]
from django.urls import re_path
from .views import SystemAPIView

urlpatterns = [
  re_path(r'^systems/?$', SystemAPIView.as_view(), name='systems'),
  re_path(r'^systems/(?P<pk>\d+)/?$', SystemAPIView.as_view(), name='system-detail'),
]
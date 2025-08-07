from django.urls import re_path
from .views import JobPositionAPIView

urlpatterns = [
  re_path(r'^job-positions/?$', JobPositionAPIView.as_view(), name='job-positions'),
  re_path(r'^job-positions/(?P<pk>\d+)/?$', JobPositionAPIView.as_view(), name='job-position-detail'),
]
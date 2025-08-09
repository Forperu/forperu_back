from django.urls import re_path
from .views import AttendanceAPIView

urlpatterns = [
  re_path(r'^attendances/?$', AttendanceAPIView.as_view(), name='attendances'),
  re_path(r'^attendances/(?P<pk>\d+)/?$', AttendanceAPIView.as_view(), name='attendance-detail'),
]
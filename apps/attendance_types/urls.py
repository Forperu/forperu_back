from django.urls import re_path
from .views import AttendanceTypeAPIView

urlpatterns = [
  re_path(r'^attendance-types/?$', AttendanceTypeAPIView.as_view(), name='attendance-types'),
  re_path(r'^attendance-types/(?P<pk>\d+)/?$', AttendanceTypeAPIView.as_view(), name='attendance-type-detail'),
]
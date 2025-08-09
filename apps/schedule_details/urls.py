from django.urls import re_path
from .views import ScheduleDetailAPIView

urlpatterns = [
  re_path(r'^schedule-details/?$', ScheduleDetailAPIView.as_view(), name='schedule-details'),
  re_path(r'^schedule-details/(?P<pk>\d+)/?$', ScheduleDetailAPIView.as_view(), name='schedule-detail-detail'),
]
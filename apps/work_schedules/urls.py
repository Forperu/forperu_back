from django.urls import re_path
from .views import WorkScheduleAPIView

urlpatterns = [
  re_path(r'^work-schedules/?$', WorkScheduleAPIView.as_view(), name='work-schedules'),
  re_path(r'^work-schedules/(?P<pk>\d+)/?$', WorkScheduleAPIView.as_view(), name='work-schedule-detail'),
]
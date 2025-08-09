from django.urls import re_path
from .views import EmployeeScheduleAPIView

urlpatterns = [
  re_path(r'^employee-schedules/?$', EmployeeScheduleAPIView.as_view(), name='employee-schedules'),
  re_path(r'^employee-schedules/(?P<pk>\d+)/?$', EmployeeScheduleAPIView.as_view(), name='employee-schedule-detail'),
]
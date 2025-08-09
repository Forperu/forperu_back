from django.urls import re_path
from .views import EmployeeIncidentAPIView

urlpatterns = [
  re_path(r'^employee-incidents/?$', EmployeeIncidentAPIView.as_view(), name='employee-incidents'),
  re_path(r'^employee-incidents/(?P<pk>\d+)/?$', EmployeeIncidentAPIView.as_view(), name='employee-incident-detail'),
]
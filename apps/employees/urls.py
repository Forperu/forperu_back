from django.urls import re_path
from .views import EmployeeAPIView

urlpatterns = [
  re_path(r'^employees/?$', EmployeeAPIView.as_view(), name='employees'),
  re_path(r'^employees/(?P<pk>\d+)/?$', EmployeeAPIView.as_view(), name='employee-detail'),
]
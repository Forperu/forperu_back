from django.urls import re_path
from .views import PayrollAPIView

urlpatterns = [
  re_path(r'^payrolls/?$', PayrollAPIView.as_view(), name='payrolls'),
  re_path(r'^payrolls/(?P<pk>\d+)/?$', PayrollAPIView.as_view(), name='payroll-detail'),
]
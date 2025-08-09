from django.urls import re_path
from .views import OvertimeRequestAPIView

urlpatterns = [
  re_path(r'^overtime-requests/?$', OvertimeRequestAPIView.as_view(), name='overtime-requests'),
  re_path(r'^overtime-requests/(?P<pk>\d+)/?$', OvertimeRequestAPIView.as_view(), name='overtime-request-detail'),
]
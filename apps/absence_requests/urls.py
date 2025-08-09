from django.urls import re_path
from .views import AbsenceRequestAPIView

urlpatterns = [
  re_path(r'^absence-requests/?$', AbsenceRequestAPIView.as_view(), name='absence-requests'),
  re_path(r'^absence-requests/(?P<pk>\d+)/?$', AbsenceRequestAPIView.as_view(), name='absence-request-detail'),
]
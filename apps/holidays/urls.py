from django.urls import re_path
from .views import HolidayAPIView

urlpatterns = [
  re_path(r'^holidays/?$', HolidayAPIView.as_view(), name='holidays'),
  re_path(r'^holidays/(?P<pk>\d+)/?$', HolidayAPIView.as_view(), name='holiday-detail'),
]
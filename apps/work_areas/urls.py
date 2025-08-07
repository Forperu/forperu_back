from django.urls import re_path
from .views import WorkAreaAPIView

urlpatterns = [
  re_path(r'^work-areas/?$', WorkAreaAPIView.as_view(), name='work-areas'),
  re_path(r'^work-areas/(?P<pk>\d+)/?$', WorkAreaAPIView.as_view(), name='work-area-detail'),
]
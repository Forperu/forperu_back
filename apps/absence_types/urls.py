from django.urls import re_path
from .views import AbsenceTypeAPIView

urlpatterns = [
  re_path(r'^absence-types/?$', AbsenceTypeAPIView.as_view(), name='absence-types'),
  re_path(r'^absence-types/(?P<pk>\d+)/?$', AbsenceTypeAPIView.as_view(), name='absence-type-detail'),
]
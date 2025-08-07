from django.urls import re_path
from .views import UnitOfMeasurementAPIView

urlpatterns = [
  re_path(r'^units-of-measurement/?$', UnitOfMeasurementAPIView.as_view(), name='units-of-measurement'),
  re_path(r'^units-of-measurement/(?P<pk>\d+)/?$', UnitOfMeasurementAPIView.as_view(), name='units-of-measurement-detail'),
]
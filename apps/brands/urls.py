from django.urls import re_path
from .views import BrandAPIView

urlpatterns = [
  re_path(r'^brands/?$', BrandAPIView.as_view(), name='brands'),
  re_path(r'^brands/(?P<pk>\d+)/?$', BrandAPIView.as_view(), name='brand-detail'),
]
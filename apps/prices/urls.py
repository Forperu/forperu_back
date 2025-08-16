from django.urls import re_path
from .views import PriceAPIView

urlpatterns = [
  re_path(r'^prices/?$', PriceAPIView.as_view(), name='prices'),
  re_path(r'^prices/(?P<pk>\d+)/?$', PriceAPIView.as_view(), name='price-detail'),
]
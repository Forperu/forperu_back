from django.urls import re_path
from .views import ExchangeRateAPIView

urlpatterns = [
  re_path(r'^exchange-rates/?$', ExchangeRateAPIView.as_view(), name='exchange-rates'),
  re_path(r'^exchange-rates/(?P<pk>\d+)/?$', ExchangeRateAPIView.as_view(), name='exchange-rate-detail'),
]
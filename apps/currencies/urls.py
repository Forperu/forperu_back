from django.urls import re_path
from .views import CurrencyAPIView

urlpatterns = [
  re_path(r'^currencies/?$', CurrencyAPIView.as_view(), name='currencies'),
  re_path(r'^currencies/(?P<pk>\d+)/?$', CurrencyAPIView.as_view(), name='currency-detail'),
]
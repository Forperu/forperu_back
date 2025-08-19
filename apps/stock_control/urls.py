from django.urls import re_path
from .views import StockControlAPIView

urlpatterns = [
  re_path(r'^stock-control/?$', StockControlAPIView.as_view(), name='stock-control'),
  re_path(r'^stock-control/(?P<pk>\d+)/?$', StockControlAPIView.as_view(), name='stock-control-detail'),
]
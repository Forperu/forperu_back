from django.urls import re_path
from .views import WarehouseAPIView

urlpatterns = [
  re_path(r'^warehouses/?$', WarehouseAPIView.as_view(), name='warehouses'),
  re_path(r'^warehouses/(?P<pk>\d+)/?$', WarehouseAPIView.as_view(), name='warehouse-detail'),
]
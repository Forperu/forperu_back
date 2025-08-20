from django.urls import re_path
from .views import InventoryMovementAPIView

urlpatterns = [
  re_path(r'^inventory-movements/?$', InventoryMovementAPIView.as_view(), name='inventory-movements'),
  re_path(r'^inventory-movements/(?P<pk>\d+)/?$', InventoryMovementAPIView.as_view(), name='inventory-movement-detail'),
]
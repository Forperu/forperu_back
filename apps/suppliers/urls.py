from django.urls import re_path
from .views import SupplierAPIView

urlpatterns = [
  re_path(r'^suppliers/?$', SupplierAPIView.as_view(), name='suppliers'),
  re_path(r'^suppliers/(?P<pk>\d+)/?$', SupplierAPIView.as_view(), name='supplier-detail'),
]
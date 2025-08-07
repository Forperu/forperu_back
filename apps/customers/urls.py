from django.urls import re_path
from .views import CustomerAPIView

urlpatterns = [
  re_path(r'^customers/?$', CustomerAPIView.as_view(), name='customers'),
  re_path(r'^customers/(?P<pk>\d+)/?$', CustomerAPIView.as_view(), name='customer-detail'),
]
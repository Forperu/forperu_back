from django.urls import re_path
from .views import PaymentMethodAPIView

urlpatterns = [
  re_path(r'^payment-methods/?$', PaymentMethodAPIView.as_view(), name='payment-methods'),
  re_path(r'^payment-methods/(?P<pk>\d+)/?$', PaymentMethodAPIView.as_view(), name='payment-method-detail'),
]
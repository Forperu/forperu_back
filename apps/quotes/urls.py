from django.urls import re_path
from .views import QuoteAPIView

urlpatterns = [
  re_path(r'^quotes/?$', QuoteAPIView.as_view(), name='quotes'),
  re_path(r'^quotes/(?P<pk>\d+)/?$', QuoteAPIView.as_view(), name='quote-detail'),
]
from django.urls import re_path
from .views import CompanyAPIView

urlpatterns = [
  re_path(r'^companies/?$', CompanyAPIView.as_view(), name='companies'),
  re_path(r'^companies/(?P<pk>\d+)/?$', CompanyAPIView.as_view(), name='company-detail'),
]
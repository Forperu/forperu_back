from django.urls import path
from .views import (
  CompanyViewSet,
  CompanyUpdate
)

urlpatterns = [
  path('companies', CompanyViewSet.as_view(), name='companies-list'),
  path('companies/<int:pk>', CompanyUpdate.as_view(), name='companies-update'),
]
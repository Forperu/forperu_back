from django.urls import re_path
from .views import EmployeeBenefitAPIView

urlpatterns = [
  re_path(r'^employee-benefits/?$', EmployeeBenefitAPIView.as_view(), name='employee-benefits'),
  re_path(r'^employee-benefits/(?P<pk>\d+)/?$', EmployeeBenefitAPIView.as_view(), name='employee-benefit-detail'),
]
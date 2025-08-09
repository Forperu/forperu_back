from django.urls import re_path
from .views import VacationBalanceAPIView

urlpatterns = [
  re_path(r'^vacation-balances/?$', VacationBalanceAPIView.as_view(), name='vacation-balances'),
  re_path(r'^vacation-balances/(?P<pk>\d+)/?$', VacationBalanceAPIView.as_view(), name='vacation-balance-detail'),
]
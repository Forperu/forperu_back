from django.urls import re_path
from .views import VacationAPIView

urlpatterns = [
  re_path(r'^vacations/?$', VacationAPIView.as_view(), name='vacations'),
  re_path(r'^vacations/(?P<pk>\d+)/?$', VacationAPIView.as_view(), name='vacation-detail'),
]
from django.urls import re_path
from .views import BranchOfficeAPIView

urlpatterns = [
  re_path(r'^branch-offices/?$', BranchOfficeAPIView.as_view(), name='branch-offices'),
  re_path(r'^branch-offices/(?P<pk>\d+)/?$', BranchOfficeAPIView.as_view(), name='branch-office-detail'),
]
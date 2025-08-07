from django.urls import re_path
from .views import RoleAPIView

urlpatterns = [
  re_path(r'^roles/?$', RoleAPIView.as_view(), name='roles'),
  re_path(r'^roles/(?P<pk>\d+)/?$', RoleAPIView.as_view(), name='role-detail'),
]
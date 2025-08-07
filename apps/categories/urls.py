from django.urls import re_path
from .views import CategoryAPIView

urlpatterns = [
  re_path(r'^categories/?$', CategoryAPIView.as_view(), name='categories'),
  re_path(r'^categories/(?P<pk>\d+)/?$', CategoryAPIView.as_view(), name='category-detail'),
]
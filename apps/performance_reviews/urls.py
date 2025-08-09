from django.urls import re_path
from .views import PerformanceReviewAPIView

urlpatterns = [
  re_path(r'^performance-reviews/?$', PerformanceReviewAPIView.as_view(), name='performance-reviews'),
  re_path(r'^performance-reviews/(?P<pk>\d+)/?$', PerformanceReviewAPIView.as_view(), name='performance-review-detail'),
]
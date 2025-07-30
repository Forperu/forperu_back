from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.brands.views import BrandViewSet
from apps.categories.views import CategoryViewSet
from apps.products.views import ProductViewSet

router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')

api_urlpatterns = [
  path('', include(router.urls)),
]
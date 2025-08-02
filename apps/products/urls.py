from django.urls import re_path
from .views import (
  ProductsView,
  ProductDetailView,
  CreateProductView,
  UpdateProductView,
  DeleteProductView,
  DeleteProductsByIdsView,
  ImportProductsView,
  ExportProductsView,
)

urlpatterns = [
  re_path(r'^products/?$', ProductsView.as_view(), name='products-list'),
  re_path(r'^products/(?P<pk>\d+)/?$', ProductDetailView.as_view(), name='product-detail'),
  re_path(r'^products/create/?$', CreateProductView.as_view(), name='product-create'),
  re_path(r'^products/(?P<pk>\d+)/update/?$', UpdateProductView.as_view(), name='product-update'),
  re_path(r'^products/(?P<pk>\d+)/delete/?$', DeleteProductView.as_view(), name='product-delete'),
  re_path(r'^products/delete/?$', DeleteProductsByIdsView.as_view(), name='product-delete'),
  re_path(r'^products/import-excel/?$', ImportProductsView.as_view(), name='product-import'),
  re_path(r'^products/export-excel/?$', ExportProductsView.as_view(), name='product-export'),
]
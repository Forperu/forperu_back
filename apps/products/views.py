from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from apps.products.models import Product
from apps.products.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
  serializer_class = ProductSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    # Solo productos activos (no eliminados)
    return Product.objects.filter(deleted_at__isnull=True)

  def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)

  def perform_update(self, serializer):
    serializer.save(updated_by=self.request.user)

  def perform_destroy(self, instance):
    instance.deleted_at = timezone.now()
    instance.updated_by = self.request.user
    instance.save()
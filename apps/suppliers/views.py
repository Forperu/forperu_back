from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.suppliers.models import Supplier
from apps.suppliers.serializers import SupplierSerializer
from django.utils import timezone

class SupplierViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Supplier.objects.filter(deleted_at__isnull=True)
    serializer = SupplierSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = Supplier.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = SupplierSerializer(category)
      return Response(serializer.data)
    except Supplier.DoesNotExist:
      return Response({'error': 'Supplier not found'}, status=404)

  def create(self, request):
    serializer = SupplierSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      category = Supplier.objects.get(pk=pk, deleted_at__isnull=True)
    except Supplier.DoesNotExist:
      return Response({'error': 'Supplier not found'}, status=404)

    serializer = SupplierSerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = Supplier.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'Supplier deleted successfully'})
    except Supplier.DoesNotExist:
      return Response({'error': 'Supplier not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Supplier.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All suppliers deleted successfully'})
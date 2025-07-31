from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.warehouses.models import Warehouse
from apps.warehouses.serializers import WarehouseSerializer
from django.utils import timezone

class WarehouseViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Warehouse.objects.filter(deleted_at__isnull=True)
    serializer = WarehouseSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
      try:
        brand = Warehouse.objects.get(pk=pk, deleted_at__isnull=True)
        serializer = WarehouseSerializer(brand)
        return Response(serializer.data)
      except Warehouse.DoesNotExist:
        return Response({'error': 'Warehouse not found'}, status=404)

  def create(self, request):
    serializer = WarehouseSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      brand = Warehouse.objects.get(pk=pk, deleted_at__isnull=True)
    except Warehouse.DoesNotExist:
      return Response({'error': 'Warehouse not found'}, status=404)

    serializer = WarehouseSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      brand = Warehouse.objects.get(pk=pk, deleted_at__isnull=True)
      brand.deleted_at = timezone.now()
      brand.save()
      return Response({'message': 'Warehouse deleted successfully'})
    except Warehouse.DoesNotExist:
      return Response({'error': 'Warehouse not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Warehouse.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All warehouses deleted successfully'})
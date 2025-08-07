import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.warehouses.models import Warehouse
from apps.warehouses.serializers import WarehouseSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class WarehouseAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un almacén
      warehouse = get_object_or_404(Warehouse, pk=pk, deleted_at__isnull=True)
      serializer = WarehouseSerializer(warehouse)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de almacenes
    warehouses = Warehouse.objects.filter(deleted_at__isnull=True)
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nuevo almacén
    serializer = WarehouseSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    warehouse = get_object_or_404(Warehouse, pk=pk, deleted_at__isnull=True)
    serializer = WarehouseSerializer(warehouse, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    warehouse = get_object_or_404(Warehouse, pk=pk, deleted_at__isnull=True)
    serializer = WarehouseSerializer(warehouse, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      warehouse = get_object_or_404(Warehouse, pk=pk, deleted_at__isnull=True)
      warehouse.deleted_at = timezone.now()
      warehouse.updated_by = request.user
      warehouse.save()
      return Response(
        {'message': 'Warehouse deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      warehouse_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not warehouse_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de almacenes'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        warehouse_ids = [int(id) for id in warehouse_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_warehouses = Warehouse.objects.filter(
        id__in=warehouse_ids,
        deleted_at__isnull=True
      )

      if existing_warehouses.count() != len(warehouse_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_warehouses.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} almacenes eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar almacenes: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.suppliers.models import Supplier
from apps.suppliers.serializers import SupplierSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class SupplierAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un proveedor
      supplier = get_object_or_404(Supplier, pk=pk, deleted_at__isnull=True)
      serializer = SupplierSerializer(supplier)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de proveedores
    suppliers = Supplier.objects.filter(deleted_at__isnull=True)
    serializer = SupplierSerializer(suppliers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nuevo proveedor
    serializer = SupplierSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    supplier = get_object_or_404(Supplier, pk=pk, deleted_at__isnull=True)
    serializer = SupplierSerializer(supplier, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    supplier = get_object_or_404(Supplier, pk=pk, deleted_at__isnull=True)
    serializer = SupplierSerializer(supplier, data=request.data, partial=True)
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
      supplier = get_object_or_404(Supplier, pk=pk, deleted_at__isnull=True)
      supplier.deleted_at = timezone.now()
      supplier.updated_by = request.user
      supplier.save()
      return Response(
        {'message': 'Supplier deleted successfully'},
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      supplier_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not supplier_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de proveedores'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        supplier_ids = [int(id) for id in supplier_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_suppliers = Supplier.objects.filter(
        id__in=supplier_ids,
        deleted_at__isnull=True
      )

      if existing_suppliers.count() != len(supplier_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_suppliers.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} proveedores eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar proveedores: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
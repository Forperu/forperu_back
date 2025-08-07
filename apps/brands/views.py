import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.brands.models import Brand
from apps.brands.serializers import BrandSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class BrandAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una marca
      brand = get_object_or_404(Brand, pk=pk, deleted_at__isnull=True)
      serializer = BrandSerializer(brand)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de marcas
    brands = Brand.objects.filter(deleted_at__isnull=True)
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva marca
    serializer = BrandSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    brand = get_object_or_404(Brand, pk=pk, deleted_at__isnull=True)
    serializer = BrandSerializer(brand, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    brand = get_object_or_404(Brand, pk=pk, deleted_at__isnull=True)
    serializer = BrandSerializer(brand, data=request.data, partial=True)
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
      brand = get_object_or_404(Brand, pk=pk, deleted_at__isnull=True)
      brand.deleted_at = timezone.now()
      brand.updated_by = request.user
      brand.save()
      return Response(
        {'message': 'Brand deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      brand_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not brand_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de compañías'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        brand_ids = [int(id) for id in brand_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_brands = Brand.objects.filter(
        id__in=brand_ids,
        deleted_at__isnull=True
      )

      if existing_brands.count() != len(brand_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_brands.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} marcas eliminadas exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar compañías: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class CategoryAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una compañía
      category = get_object_or_404(Category, pk=pk, deleted_at__isnull=True)
      serializer = CategorySerializer(category)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Listado de categorías
    companies = Category.objects.filter(deleted_at__isnull=True)
    serializer = CategorySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva categoría
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    category = get_object_or_404(Category, pk=pk, deleted_at__isnull=True)
    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    category = get_object_or_404(Category, pk=pk, deleted_at__isnull=True)
    serializer = CategorySerializer(category, data=request.data, partial=True)
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
      category = get_object_or_404(Category, pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.updated_by = request.user
      category.save()
      return Response(
        {'message': 'Category deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      category_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])
      
      if not category_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de categorías'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        category_ids = [int(id) for id in category_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de categorías no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_companies = Category.objects.filter(
        id__in=category_ids,
        deleted_at__isnull=True
      )

      if existing_companies.count() != len(category_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_companies.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} categorías eliminadas exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar categorías: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from django.utils import timezone

class CategoryViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Category.objects.filter(deleted_at__isnull=True)
    serializer = CategorySerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = Category.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = CategorySerializer(category)
      return Response(serializer.data)
    except Category.DoesNotExist:
      return Response({'error': 'Category not found'}, status=404)

  def create(self, request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      category = Category.objects.get(pk=pk, deleted_at__isnull=True)
    except Category.DoesNotExist:
      return Response({'error': 'Category not found'}, status=404)

    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = Category.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'Category deleted successfully'})
    except Category.DoesNotExist:
      return Response({'error': 'Category not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Category.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All categories deleted successfully'})
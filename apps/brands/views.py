from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.brands.models import Brand
from apps.brands.serializers import BrandSerializer
from django.utils import timezone

class BrandViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Brand.objects.filter(deleted_at__isnull=True)
    serializer = BrandSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
      try:
        brand = Brand.objects.get(pk=pk, deleted_at__isnull=True)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)
      except Brand.DoesNotExist:
        return Response({'error': 'Brand not found'}, status=404)

  def create(self, request):
    serializer = BrandSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      brand = Brand.objects.get(pk=pk, deleted_at__isnull=True)
    except Brand.DoesNotExist:
      return Response({'error': 'Brand not found'}, status=404)

    serializer = BrandSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      brand = Brand.objects.get(pk=pk, deleted_at__isnull=True)
      brand.deleted_at = timezone.now()
      brand.save()
      return Response({'message': 'Brand deleted successfully'})
    except Brand.DoesNotExist:
      return Response({'error': 'Brand not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Brand.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All brands deleted successfully'})
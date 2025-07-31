from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.job_positions.models import JobPosition
from apps.job_positions.serializers import JobPositionSerializer
from django.utils import timezone

class JobPositionViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = JobPosition.objects.filter(deleted_at__isnull=True)
    serializer = JobPositionSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
      try:
        brand = JobPosition.objects.get(pk=pk, deleted_at__isnull=True)
        serializer = JobPositionSerializer(brand)
        return Response(serializer.data)
      except JobPosition.DoesNotExist:
        return Response({'error': 'JobPosition not found'}, status=404)

  def create(self, request):
    serializer = JobPositionSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      brand = JobPosition.objects.get(pk=pk, deleted_at__isnull=True)
    except JobPosition.DoesNotExist:
      return Response({'error': 'JobPosition not found'}, status=404)

    serializer = JobPositionSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      brand = JobPosition.objects.get(pk=pk, deleted_at__isnull=True)
      brand.deleted_at = timezone.now()
      brand.save()
      return Response({'message': 'JobPosition deleted successfully'})
    except JobPosition.DoesNotExist:
      return Response({'error': 'JobPosition not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    JobPosition.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All job_positions deleted successfully'})
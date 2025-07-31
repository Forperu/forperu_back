from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.work_areas.models import WorkArea
from apps.work_areas.serializers import WorkAreaSerializer
from django.utils import timezone

class WorkAreaViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = WorkArea.objects.filter(deleted_at__isnull=True)
    serializer = WorkAreaSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
      try:
        brand = WorkArea.objects.get(pk=pk, deleted_at__isnull=True)
        serializer = WorkAreaSerializer(brand)
        return Response(serializer.data)
      except WorkArea.DoesNotExist:
        return Response({'error': 'WorkArea not found'}, status=404)

  def create(self, request):
    serializer = WorkAreaSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      brand = WorkArea.objects.get(pk=pk, deleted_at__isnull=True)
    except WorkArea.DoesNotExist:
      return Response({'error': 'WorkArea not found'}, status=404)

    serializer = WorkAreaSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      brand = WorkArea.objects.get(pk=pk, deleted_at__isnull=True)
      brand.deleted_at = timezone.now()
      brand.save()
      return Response({'message': 'WorkArea deleted successfully'})
    except WorkArea.DoesNotExist:
      return Response({'error': 'WorkArea not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    WorkArea.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All work_areas deleted successfully'})
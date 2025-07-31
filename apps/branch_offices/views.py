from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.branch_offices.models import BranchOffice
from apps.branch_offices.serializers import BranchOfficeSerializer
from django.utils import timezone

class BranchOfficeViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = BranchOffice.objects.filter(deleted_at__isnull=True)
    serializer = BranchOfficeSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      brand = BranchOffice.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = BranchOfficeSerializer(brand)
      return Response(serializer.data)
    except BranchOffice.DoesNotExist:
      return Response({'error': 'BranchOffice not found'}, status=404)

  def create(self, request):
    serializer = BranchOfficeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      brand = BranchOffice.objects.get(pk=pk, deleted_at__isnull=True)
    except BranchOffice.DoesNotExist:
      return Response({'error': 'BranchOffice not found'}, status=404)

    serializer = BranchOfficeSerializer(brand, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      brand = BranchOffice.objects.get(pk=pk, deleted_at__isnull=True)
      brand.deleted_at = timezone.now()
      brand.save()
      return Response({'message': 'BranchOffice deleted successfully'})
    except BranchOffice.DoesNotExist:
      return Response({'error': 'BranchOffice not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    BranchOffice.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All branch_offices deleted successfully'})
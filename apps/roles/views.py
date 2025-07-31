from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.roles.models import Role
from apps.roles.serializers import RoleSerializer
from django.utils import timezone

class RoleViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Role.objects.filter(deleted_at__isnull=True)
    serializer = RoleSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      unitOfMeasurement = Role.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = RoleSerializer(unitOfMeasurement)
      return Response(serializer.data)
    except Role.DoesNotExist:
      return Response({'error': 'Role not found'}, status=404)

  def create(self, request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      unitOfMeasurement = Role.objects.get(pk=pk, deleted_at__isnull=True)
    except Role.DoesNotExist:
      return Response({'error': 'Role not found'}, status=404)

    serializer = RoleSerializer(unitOfMeasurement, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      unitOfMeasurement = Role.objects.get(pk=pk, deleted_at__isnull=True)
      unitOfMeasurement.deleted_at = timezone.now()
      unitOfMeasurement.save()
      return Response({'message': 'Role deleted successfully'})
    except Role.DoesNotExist:
      return Response({'error': 'Role not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Role.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All roles deleted successfully'})
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer
from django.utils import timezone

class EmployeeViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Employee.objects.filter(deleted_at__isnull=True)
    serializer = EmployeeSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = Employee.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = EmployeeSerializer(category)
      return Response(serializer.data)
    except Employee.DoesNotExist:
      return Response({'error': 'Employee not found'}, status=404)

  def create(self, request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      category = Employee.objects.get(pk=pk, deleted_at__isnull=True)
    except Employee.DoesNotExist:
      return Response({'error': 'Employee not found'}, status=404)

    serializer = EmployeeSerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = Employee.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'Employee deleted successfully'})
    except Employee.DoesNotExist:
      return Response({'error': 'Employee not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Employee.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All employees deleted successfully'})
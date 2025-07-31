from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer
from django.utils import timezone

class CustomerViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Customer.objects.filter(deleted_at__isnull=True)
    serializer = CustomerSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = Customer.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = CustomerSerializer(category)
      return Response(serializer.data)
    except Customer.DoesNotExist:
      return Response({'error': 'Customer not found'}, status=404)

  def create(self, request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      category = Customer.objects.get(pk=pk, deleted_at__isnull=True)
    except Customer.DoesNotExist:
      return Response({'error': 'Customer not found'}, status=404)

    serializer = CustomerSerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = Customer.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'Customer deleted successfully'})
    except Customer.DoesNotExist:
      return Response({'error': 'Customer not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Customer.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All customers deleted successfully'})
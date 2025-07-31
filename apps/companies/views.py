from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from django.utils import timezone

class CompanyViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Company.objects.filter(deleted_at__isnull=True)
    serializer = CompanySerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = Company.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = CompanySerializer(category)
      return Response(serializer.data)
    except Company.DoesNotExist:
      return Response({'error': 'Company not found'}, status=404)

  def create(self, request):
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = Company.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'Company deleted successfully'})
    except Company.DoesNotExist:
      return Response({'error': 'Company not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Company.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All companies deleted successfully'})
  
class CompanyUpdate(viewsets.ViewSet):
  
  def update(self, request, pk=None):
    try:
      company = Company.objects.get(pk=pk, deleted_at__isnull=True)
    except Company.DoesNotExist:
      return Response({'error': 'Company not found'}, status=404)

    serializer = CompanySerializer(company, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)
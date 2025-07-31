from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.currencies.models import Currency
from apps.currencies.serializers import CurrencySerializer
from django.utils import timezone

class CurrencyViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = Currency.objects.filter(deleted_at__isnull=True)
    serializer = CurrencySerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = Currency.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = CurrencySerializer(category)
      return Response(serializer.data)
    except Currency.DoesNotExist:
      return Response({'error': 'Currency not found'}, status=404)

  def create(self, request):
    serializer = CurrencySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      category = Currency.objects.get(pk=pk, deleted_at__isnull=True)
    except Currency.DoesNotExist:
      return Response({'error': 'Currency not found'}, status=404)

    serializer = CurrencySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = Currency.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'Currency deleted successfully'})
    except Currency.DoesNotExist:
      return Response({'error': 'Currency not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    Currency.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All currencies deleted successfully'})
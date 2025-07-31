from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.exchange_rates.models import ExchangeRate
from apps.exchange_rates.serializers import ExchangeRateSerializer
from django.utils import timezone

class ExchangeRateViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = ExchangeRate.objects.filter(deleted_at__isnull=True)
    serializer = ExchangeRateSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = ExchangeRate.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = ExchangeRateSerializer(category)
      return Response(serializer.data)
    except ExchangeRate.DoesNotExist:
      return Response({'error': 'ExchangeRate not found'}, status=404)

  def create(self, request):
    serializer = ExchangeRateSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      category = ExchangeRate.objects.get(pk=pk, deleted_at__isnull=True)
    except ExchangeRate.DoesNotExist:
      return Response({'error': 'ExchangeRate not found'}, status=404)

    serializer = ExchangeRateSerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = ExchangeRate.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'ExchangeRate deleted successfully'})
    except ExchangeRate.DoesNotExist:
      return Response({'error': 'ExchangeRate not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    ExchangeRate.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All exchange_rates deleted successfully'})
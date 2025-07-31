from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.payment_methods.models import PaymentMethod
from apps.payment_methods.serializers import PaymentMethodSerializer
from django.utils import timezone

class PaymentMethodViewSet(viewsets.ViewSet):

  def list(self, request):
    queryset = PaymentMethod.objects.filter(deleted_at__isnull=True)
    serializer = PaymentMethodSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    try:
      category = PaymentMethod.objects.get(pk=pk, deleted_at__isnull=True)
      serializer = PaymentMethodSerializer(category)
      return Response(serializer.data)
    except PaymentMethod.DoesNotExist:
      return Response({'error': 'PaymentMethod not found'}, status=404)

  def create(self, request):
    serializer = PaymentMethodSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    try:
      category = PaymentMethod.objects.get(pk=pk, deleted_at__isnull=True)
    except PaymentMethod.DoesNotExist:
      return Response({'error': 'PaymentMethod not found'}, status=404)

    serializer = PaymentMethodSerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data)
    return Response(serializer.errors, status=400)

  def destroy(self, request, pk=None):
    try:
      category = PaymentMethod.objects.get(pk=pk, deleted_at__isnull=True)
      category.deleted_at = timezone.now()
      category.save()
      return Response({'message': 'PaymentMethod deleted successfully'})
    except PaymentMethod.DoesNotExist:
      return Response({'error': 'PaymentMethod not found'}, status=404)

  @action(detail=False, methods=['delete'])
  def delete_all(self, request):
    PaymentMethod.objects.filter(deleted_at__isnull=True).update(deleted_at=timezone.now())
    return Response({'message': 'All payment_methods deleted successfully'})
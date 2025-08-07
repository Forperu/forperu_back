import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.exchange_rates.models import ExchangeRate
from apps.exchange_rates.serializers import ExchangeRateSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class ExchangeRateAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un tipo de cambio
      exchangeRate = get_object_or_404(ExchangeRate, pk=pk, deleted_at__isnull=True)
      serializer = ExchangeRateSerializer(exchangeRate)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de tipo de cambios
    exchangeRates = ExchangeRate.objects.filter(deleted_at__isnull=True)
    serializer = ExchangeRateSerializer(exchangeRates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nuevo tipo de cambio
    serializer = ExchangeRateSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    exchangeRate = get_object_or_404(ExchangeRate, pk=pk, deleted_at__isnull=True)
    serializer = ExchangeRateSerializer(exchangeRate, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    exchangeRate = get_object_or_404(ExchangeRate, pk=pk, deleted_at__isnull=True)
    serializer = ExchangeRateSerializer(exchangeRate, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      exchangeRate = get_object_or_404(ExchangeRate, pk=pk, deleted_at__isnull=True)
      exchangeRate.deleted_at = timezone.now()
      exchangeRate.updated_by = request.user
      exchangeRate.save()
      return Response(
        {'message': 'ExchangeRate deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      exchangeRate_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not exchangeRate_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de tipo de cambios'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        exchangeRate_ids = [int(id) for id in exchangeRate_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_ExchangeRates = ExchangeRate.objects.filter(
        id__in=exchangeRate_ids,
        deleted_at__isnull=True
      )

      if existing_ExchangeRates.count() != len(exchangeRate_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_ExchangeRates.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} tipo de cambios eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar tipo de cambios: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
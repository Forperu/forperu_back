import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.currencies.models import Currency
from apps.currencies.serializers import CurrencySerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class CurrencyAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una moneda
      currency = get_object_or_404(Currency, pk=pk, deleted_at__isnull=True)
      serializer = CurrencySerializer(currency)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de monedas
    currencies = Currency.objects.filter(deleted_at__isnull=True)
    serializer = CurrencySerializer(currencies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva moneda
    serializer = CurrencySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    currency = get_object_or_404(Currency, pk=pk, deleted_at__isnull=True)
    serializer = CurrencySerializer(currency, data=request.data)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    currency = get_object_or_404(Currency, pk=pk, deleted_at__isnull=True)
    serializer = CurrencySerializer(currency, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      currency = get_object_or_404(Currency, pk=pk, deleted_at__isnull=True)
      currency.deleted_at = timezone.now()
      currency.save()
      return Response(
        {'message': 'Currency deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      currency_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not currency_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de monedas'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        currency_ids = [int(id) for id in currency_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_currencies = Currency.objects.filter(
        id__in=currency_ids,
        deleted_at__isnull=True
      )

      if existing_currencies.count() != len(currency_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_currencies.update(deleted_at=timezone.now())

      return Response({
        'message': f'{updated} monedas eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar monedas: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
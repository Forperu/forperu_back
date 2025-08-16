import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.prices.models import Price
from apps.prices.serializers import PriceSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class PriceAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un precio
      price = get_object_or_404(Price, pk=pk, deleted_at__isnull=True)
      serializer = PriceSerializer(price)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de precios
    prices = Price.objects.filter(deleted_at__isnull=True)
    serializer = PriceSerializer(prices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nuevo precio
    serializer = PriceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    price = get_object_or_404(Price, pk=pk, deleted_at__isnull=True)
    serializer = PriceSerializer(price, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    price = get_object_or_404(Price, pk=pk, deleted_at__isnull=True)
    serializer = PriceSerializer(price, data=request.data, partial=True)
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
      price = get_object_or_404(Price, pk=pk, deleted_at__isnull=True)
      price.deleted_at = timezone.now()
      price.updated_by = request.user
      price.save()
      return Response(
        {'message': 'Price deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      price_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not price_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de precios'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        price_ids = [int(id) for id in price_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_prices = Price.objects.filter(
        id__in=price_ids,
        deleted_at__isnull=True
      )

      if existing_prices.count() != len(price_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_prices.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} precios eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar precios: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
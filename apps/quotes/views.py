import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone
from apps.quotes.models import Quote, QuoteDetail
from apps.quotes.serializers import QuoteSerializer, QuoteDetailSerializer

class QuoteAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      quote = get_object_or_404(Quote, pk=pk, deleted_at__isnull=True)
      serializer = QuoteSerializer(quote)
      return Response(serializer.data, status=status.HTTP_200_OK)

    quotes = Quote.objects.filter(deleted_at__isnull=True)
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    serializer = QuoteSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    quote = get_object_or_404(Quote, pk=pk, deleted_at__isnull=True)
    serializer = QuoteSerializer(quote, data=request.data)
    if serializer.is_valid():
      serializer.save(updated_by=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    quote = get_object_or_404(Quote, pk=pk, deleted_at__isnull=True)
    serializer = QuoteSerializer(quote, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_by=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      quote = get_object_or_404(Quote, pk=pk, deleted_at__isnull=True)
      quote.deleted_at = timezone.now()
      quote.updated_by = request.user
      quote.save()
      return Response({'message': 'Quote deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      quote_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not quote_ids:
        return Response({'error': 'No se proporcionaron IDs de cotizaciones'}, status=status.HTTP_400_BAD_REQUEST)

      try:
        quote_ids = [int(id) for id in quote_ids]
      except (ValueError, TypeError):
        return Response({'error': 'IDs de cotizaciones no válidos'}, status=status.HTTP_400_BAD_REQUEST)

      existing_quotes = Quote.objects.filter(id__in=quote_ids, deleted_at__isnull=True)

      if existing_quotes.count() != len(quote_ids):
        return Response({'error': 'Algunos IDs no existen o ya fueron eliminados'}, status=status.HTTP_400_BAD_REQUEST)

      updated = existing_quotes.update(deleted_at=timezone.now(), updated_by=request.user)

      return Response({
        'message': f'{updated} cotizaciones eliminadas exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response({'error': f'Error al eliminar cotizaciones: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuoteDetailAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      detail = get_object_or_404(QuoteDetail, pk=pk, deleted_at__isnull=True)
      serializer = QuoteDetailSerializer(detail)
      return Response(serializer.data, status=status.HTTP_200_OK)

    details = QuoteDetail.objects.filter(deleted_at__isnull=True)
    serializer = QuoteDetailSerializer(details, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    serializer = QuoteDetailSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    detail = get_object_or_404(QuoteDetail, pk=pk, deleted_at__isnull=True)
    serializer = QuoteDetailSerializer(detail, data=request.data)
    if serializer.is_valid():
      serializer.save(updated_by=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    detail = get_object_or_404(QuoteDetail, pk=pk, deleted_at__isnull=True)
    serializer = QuoteDetailSerializer(detail, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_by=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      detail = get_object_or_404(QuoteDetail, pk=pk, deleted_at__isnull=True)
      detail.deleted_at = timezone.now()
      detail.updated_by = request.user
      detail.save()
      return Response({'message': 'QuoteDetail deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      detail_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not detail_ids:
        return Response({'error': 'No se proporcionaron IDs de detalles de cotización'}, status=status.HTTP_400_BAD_REQUEST)

      try:
        detail_ids = [int(id) for id in detail_ids]
      except (ValueError, TypeError):
        return Response({'error': 'IDs de detalles no válidos'}, status=status.HTTP_400_BAD_REQUEST)

      existing_details = QuoteDetail.objects.filter(id__in=detail_ids, deleted_at__isnull=True)

      if existing_details.count() != len(detail_ids):
        return Response({'error': 'Algunos IDs no existen o ya fueron eliminados'}, status=status.HTTP_400_BAD_REQUEST)

      updated = existing_details.update(deleted_at=timezone.now(), updated_by=request.user)

      return Response({
        'message': f'{updated} detalles de cotización eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response({'error': f'Error al eliminar detalles: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

from apps.stock_control.models import StockControl
from apps.stock_control.serializers import StockControlSerializer

class StockControlAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      stock_control = get_object_or_404(StockControl, pk=pk, deleted_at__isnull=True)
      serializer = StockControlSerializer(stock_control)
      return Response(serializer.data, status=status.HTTP_200_OK)

    stock_controls = StockControl.objects.filter(deleted_at__isnull=True)
    serializer = StockControlSerializer(stock_controls, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    serializer = StockControlSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    stock_control = get_object_or_404(StockControl, pk=pk, deleted_at__isnull=True)
    serializer = StockControlSerializer(stock_control, data=request.data)
    if serializer.is_valid():
      serializer.save(updated_by=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    stock_control = get_object_or_404(StockControl, pk=pk, deleted_at__isnull=True)
    serializer = StockControlSerializer(stock_control, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_by=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      stock_control = get_object_or_404(StockControl, pk=pk, deleted_at__isnull=True)
      stock_control.deleted_at = timezone.now()
      stock_control.updated_by = request.user
      stock_control.save()
      return Response({'message': 'StockControl deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])
      if not ids:
        return Response({'error': 'No se proporcionaron IDs'}, status=status.HTTP_400_BAD_REQUEST)

      try:
        ids = [int(i) for i in ids]
      except (ValueError, TypeError):
        return Response({'error': 'IDs no válidos'}, status=status.HTTP_400_BAD_REQUEST)

      existing = StockControl.objects.filter(id__in=ids, deleted_at__isnull=True)
      if existing.count() != len(ids):
        return Response({'error': 'Algunos IDs no existen o ya fueron eliminados'}, status=status.HTTP_400_BAD_REQUEST)

      updated = existing.update(deleted_at=timezone.now(), updated_by=request.user)
      return Response({'message': f'{updated} registros eliminados', 'deleted_count': updated}, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response({'error': f'Error al eliminar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
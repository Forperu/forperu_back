import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

from apps.inventory_movements.models import InventoryMovement
from apps.inventory_movements.serializers import InventoryMovementSerializer

class InventoryMovementAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      movement = get_object_or_404(InventoryMovement, pk=pk, deleted_at__isnull=True)
      serializer = InventoryMovementSerializer(movement)
      return Response(serializer.data, status=status.HTTP_200_OK)

    movements = InventoryMovement.objects.filter(deleted_at__isnull=True)
    serializer = InventoryMovementSerializer(movements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    serializer = InventoryMovementSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user_id=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    movement = get_object_or_404(InventoryMovement, pk=pk, deleted_at__isnull=True)
    serializer = InventoryMovementSerializer(movement, data=request.data)
    if serializer.is_valid():
      serializer.save(user_id=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    movement = get_object_or_404(InventoryMovement, pk=pk, deleted_at__isnull=True)
    serializer = InventoryMovementSerializer(movement, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(user_id=request.user, updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      movement = get_object_or_404(InventoryMovement, pk=pk, deleted_at__isnull=True)
      movement.deleted_at = timezone.now()
      movement.user_id = request.user
      movement.save()
      return Response({'message': 'InventoryMovement deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
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

      existing = InventoryMovement.objects.filter(id__in=ids, deleted_at__isnull=True)
      if existing.count() != len(ids):
        return Response({'error': 'Algunos IDs no existen o ya fueron eliminados'}, status=status.HTTP_400_BAD_REQUEST)

      updated = existing.update(deleted_at=timezone.now(), user_id=request.user)
      return Response({'message': f'{updated} registros eliminados', 'deleted_count': updated}, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response({'error': f'Error al eliminar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
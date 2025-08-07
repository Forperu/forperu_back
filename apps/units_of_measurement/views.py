import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.units_of_measurement.models import UnitOfMeasurement
from apps.units_of_measurement.serializers import UnitOfMeasurementSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class UnitOfMeasurementAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una unidad de medida
      unit = get_object_or_404(UnitOfMeasurement, pk=pk, deleted_at__isnull=True)
      serializer = UnitOfMeasurementSerializer(unit)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de unidades de medida
    units = UnitOfMeasurement.objects.filter(deleted_at__isnull=True)
    serializer = UnitOfMeasurementSerializer(units, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva unidad de medida
    serializer = UnitOfMeasurementSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    unit = get_object_or_404(UnitOfMeasurement, pk=pk, deleted_at__isnull=True)
    serializer = UnitOfMeasurementSerializer(unit, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    unit = get_object_or_404(UnitOfMeasurement, pk=pk, deleted_at__isnull=True)
    serializer = UnitOfMeasurementSerializer(unit, data=request.data, partial=True)
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
      unit = get_object_or_404(UnitOfMeasurement, pk=pk, deleted_at__isnull=True)
      unit.deleted_at = timezone.now()
      unit.updated_by = request.user
      unit.save()
      return Response(
        {'message': 'UnitOfMeasuremen deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      unit_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])
      
      if not unit_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de unidades de medida'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        unit_ids = [int(id) for id in unit_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de unidades de medida no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_units = UnitOfMeasurement.objects.filter(
        id__in=unit_ids,
        deleted_at__isnull=True
      )

      if existing_units.count() != len(unit_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_units.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} unidades de medida eliminadas exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar unidades de medida: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
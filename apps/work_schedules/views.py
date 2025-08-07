import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.work_schedules.models import WorkSchedule
from apps.work_schedules.serializers import WorkScheduleSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class WorkScheduleAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una horario laboral
      attendanceType = get_object_or_404(WorkSchedule, pk=pk, deleted_at__isnull=True)
      serializer = WorkScheduleSerializer(attendanceType)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Listado de horarios laborales
    attendanceTypes = WorkSchedule.objects.filter(deleted_at__isnull=True)
    serializer = WorkScheduleSerializer(attendanceTypes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva horario laboral
    serializer = WorkScheduleSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
      # Actualización completa
      attendanceType = get_object_or_404(WorkSchedule, pk=pk, deleted_at__isnull=True)
      serializer = WorkScheduleSerializer(attendanceType, data=request.data)
      if serializer.is_valid():
        serializer.save(updated_at=timezone.now())
        return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
      # Actualización parcial
      attendanceType = get_object_or_404(WorkSchedule, pk=pk, deleted_at__isnull=True)
      serializer = WorkScheduleSerializer(attendanceType, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save(updated_at=timezone.now())
        return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      attendanceType = get_object_or_404(WorkSchedule, pk=pk, deleted_at__isnull=True)
      attendanceType.deleted_at = timezone.now()
      attendanceType.updated_by = request.user
      attendanceType.save()
      return Response(
        {'message': 'WorkSchedule deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      attendanceType_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])
      
      if not attendanceType_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de horarios laborales'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        attendanceType_ids = [int(id) for id in attendanceType_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de horarios laborales no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      axisting_WorkSchedules = WorkSchedule.objects.filter(
        id__in=attendanceType_ids,
        deleted_at__isnull=True
      )

      if axisting_WorkSchedules.count() != len(attendanceType_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = axisting_WorkSchedules.update(deleted_at=timezone.now())

      return Response({
        'message': f'{updated} horarios laborales eliminadas exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar horarios laborales: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.vacations.models import Vacation
from apps.vacations.serializers import VacationSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class VacationAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una vacación
      attendanceType = get_object_or_404(Vacation, pk=pk, deleted_at__isnull=True)
      serializer = VacationSerializer(attendanceType)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Listado de vacaciones
    attendanceTypes = Vacation.objects.filter(deleted_at__isnull=True)
    serializer = VacationSerializer(attendanceTypes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva vacación
    serializer = VacationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
      # Actualización completa
      attendanceType = get_object_or_404(Vacation, pk=pk, deleted_at__isnull=True)
      serializer = VacationSerializer(attendanceType, data=request.data)
      if serializer.is_valid():
        serializer.save(updated_at=timezone.now())
        return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
      # Actualización parcial
      attendanceType = get_object_or_404(Vacation, pk=pk, deleted_at__isnull=True)
      serializer = VacationSerializer(attendanceType, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save(updated_at=timezone.now())
        return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      attendanceType = get_object_or_404(Vacation, pk=pk, deleted_at__isnull=True)
      attendanceType.deleted_at = timezone.now()
      attendanceType.updated_by = request.user
      attendanceType.save()
      return Response(
        {'message': 'Vacation deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      attendanceType_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])
      
      if not attendanceType_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de vacaciones'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        attendanceType_ids = [int(id) for id in attendanceType_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de vacaciones no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      axisting_Vacations = Vacation.objects.filter(
        id__in=attendanceType_ids,
        deleted_at__isnull=True
      )

      if axisting_Vacations.count() != len(attendanceType_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = axisting_Vacations.update(deleted_at=timezone.now())

      return Response({
        'message': f'{updated} vacaciones eliminadas exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar vacaciones: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
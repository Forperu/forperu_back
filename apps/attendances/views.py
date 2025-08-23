import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone
from datetime import timedelta

class AttendanceAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      obj = get_object_or_404(Attendance, pk=pk, deleted_at__isnull=True)
      serializer = AttendanceSerializer(obj)
      return Response(serializer.data, status=status.HTTP_200_OK)
        
    # Obtener la fecha actual
    now = timezone.now()
    
    # Calcular el inicio de la semana actual (lunes)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Calcular el final de la semana actual (domingo)
    end_of_week = start_of_week + timedelta(days=6)
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Filtrar asistencias creadas durante esta semana
    objs = Attendance.objects.filter(
      deleted_at__isnull=True,
      date__range=(start_of_week, end_of_week)
    ).order_by('-date')
    
    serializer = AttendanceSerializer(objs, many=True)
    
    # Agregar información de la semana en la respuesta
    response_data = serializer.data
    
    return Response(response_data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    obj = get_object_or_404(Attendance, pk=pk, deleted_at__isnull=True)
    serializer = AttendanceSerializer(obj, data=request.data)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    obj = get_object_or_404(Attendance, pk=pk, deleted_at__isnull=True)
    serializer = AttendanceSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      obj = get_object_or_404(Attendance, pk=pk, deleted_at__isnull=True)
      obj.deleted_at = timezone.now()
      obj.save()
      return Response(
        {'message': 'Attendance deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])
          
      if not ids:
        return Response(
          {'error': 'No IDs provided'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        ids = [int(id) for id in ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'Invalid IDs'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_objs = Attendance.objects.filter(
        id__in=ids,
        deleted_at__isnull=True
      )

      if existing_objs.count() != len(ids):
        return Response(
          {'error': 'Some IDs do not exist or were already deleted'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_objs.update(deleted_at=timezone.now())

      return Response({
        'message': f'{updated} attendances deleted successfully',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error deleting attendances: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.job_positions.models import JobPosition
from apps.job_positions.serializers import JobPositionSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class JobPositionAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una posición laboral
      jobPosition = get_object_or_404(JobPosition, pk=pk, deleted_at__isnull=True)
      serializer = JobPositionSerializer(jobPosition)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de posiciones laborales
    jobPositions = JobPosition.objects.filter(deleted_at__isnull=True)
    serializer = JobPositionSerializer(jobPositions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva posición laboral
    serializer = JobPositionSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    jobPosition = get_object_or_404(JobPosition, pk=pk, deleted_at__isnull=True)
    serializer = JobPositionSerializer(jobPosition, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    jobPosition = get_object_or_404(JobPosition, pk=pk, deleted_at__isnull=True)
    serializer = JobPositionSerializer(jobPosition, data=request.data, partial=True)
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
      jobPosition = get_object_or_404(JobPosition, pk=pk, deleted_at__isnull=True)
      jobPosition.deleted_at = timezone.now()
      jobPosition.updated_by = request.user
      jobPosition.save()
      return Response(
        {'message': 'JobPosition deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      jobPosition_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not jobPosition_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de posiciones laborales'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        jobPosition_ids = [int(id) for id in jobPosition_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      jxisting_JobPositions = JobPosition.objects.filter(
        id__in=jobPosition_ids,
        deleted_at__isnull=True
      )

      if jxisting_JobPositions.count() != len(jobPosition_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = jxisting_JobPositions.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} posiciones laborales eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar posiciones laborales: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.work_areas.models import WorkArea
from apps.work_areas.serializers import WorkAreaSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

class WorkAreaAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un área de trabajo
      workArea = get_object_or_404(WorkArea, pk=pk, deleted_at__isnull=True)
      serializer = WorkAreaSerializer(workArea)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de áreas de trabajo
    workAreas = WorkArea.objects.filter(deleted_at__isnull=True)
    serializer = WorkAreaSerializer(workAreas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nuevo área de trabajo
    serializer = WorkAreaSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    workArea = get_object_or_404(WorkArea, pk=pk, deleted_at__isnull=True)
    serializer = WorkAreaSerializer(workArea, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    workArea = get_object_or_404(WorkArea, pk=pk, deleted_at__isnull=True)
    serializer = WorkAreaSerializer(workArea, data=request.data, partial=True)
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
      workArea = get_object_or_404(WorkArea, pk=pk, deleted_at__isnull=True)
      workArea.deleted_at = timezone.now()
      workArea.updated_by = request.user
      workArea.save()
      return Response(
        {'message': 'WorkArea deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      workArea_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not workArea_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de áreas de trabajo'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        workArea_ids = [int(id) for id in workArea_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de marcas no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_workAreas = WorkArea.objects.filter(
        id__in=workArea_ids,
        deleted_at__isnull=True
      )

      if existing_workAreas.count() != len(workArea_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_workAreas.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} áreas de trabajo eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar áreas de trabajo: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
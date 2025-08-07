import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from apps.branch_offices.models import BranchOffice
from apps.branch_offices.serializers import BranchOfficeSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

class BranchOfficeAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      branch_office = get_object_or_404(BranchOffice, pk=pk, deleted_at__isnull=True)
      serializer = BranchOfficeSerializer(branch_office)
      return Response(serializer.data, status=status.HTTP_200_OK)

    branch_offices = BranchOffice.objects.filter(deleted_at__isnull=True)
    serializer = BranchOfficeSerializer(branch_offices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    serializer = BranchOfficeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(
        created_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    branch_office = get_object_or_404(BranchOffice, pk=pk, deleted_at__isnull=True)
    serializer = BranchOfficeSerializer(branch_office, data=request.data)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    branch_office = get_object_or_404(BranchOffice, pk=pk, deleted_at__isnull=True)
    serializer = BranchOfficeSerializer(branch_office, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(
        updated_by=request.user,
        updated_at=timezone.now()
      )
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None, format=None):
    if pk:
      branch_office = get_object_or_404(BranchOffice, pk=pk, deleted_at__isnull=True)
      branch_office.deleted_at = timezone.now()
      branch_office.updated_by = request.user
      branch_office.save()
      return Response({'message': 'Sucursal eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)

    return self._delete_multiple(request)

  def _delete_multiple(self, request):
    try:
      branch_office_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not branch_office_ids:
        return Response({'error': 'No se proporcionaron IDs de sucursales'}, status=status.HTTP_400_BAD_REQUEST)

      try:
        branch_office_ids = [int(id) for id in branch_office_ids]
      except (ValueError, TypeError):
        return Response({'error': 'IDs de sucursales no válidos'}, status=status.HTTP_400_BAD_REQUEST)

      existing_branch_offices = BranchOffice.objects.filter(id__in=branch_office_ids, deleted_at__isnull=True)

      if existing_branch_offices.count() != len(branch_office_ids):
        return Response({'error': 'Algunos IDs no existen o ya fueron eliminados'}, status=status.HTTP_400_BAD_REQUEST)

      updated = existing_branch_offices.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} sucursales eliminadas exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response({'error': f'Error al eliminar sucursales: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
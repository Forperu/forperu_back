import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.roles.models import Role
from apps.roles.serializers import RoleSerializer
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

class RoleAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un rol
      role = get_object_or_404(Role, pk=pk, deleted_at__isnull=True)
      serializer = RoleSerializer(role)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de roles
    roles = Role.objects.filter(deleted_at__isnull=True)
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request, format=None):
    # Creación de nuevo rol
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def put(self, request, pk, format=None):
    # Actualización completa
    role = get_object_or_404(Role, pk=pk, deleted_at__isnull=True)
    serializer = RoleSerializer(role, data=request.data)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request, pk, format=None):
    # Actualización parcial
    role = get_object_or_404(Role, pk=pk, deleted_at__isnull=True)
    serializer = RoleSerializer(role, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_at=timezone.now())
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      role = get_object_or_404(Role, pk=pk, deleted_at__isnull=True)
      role.deleted_at = timezone.now()
      role.save()
      return Response(
        {'message': 'Role deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)
  
  def _delete_multiple(self, request):
    try:
      role_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not role_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de roles'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        role_ids = [int(id) for id in role_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de roles no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_roles = Role.objects.filter(
        id__in=role_ids,
        deleted_at__isnull=True
      )

      if existing_roles.count() != len(role_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_roles.update(
        deleted_at=timezone.now()
      )

      return Response({
        'message': f'{updated} roles eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar roles: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
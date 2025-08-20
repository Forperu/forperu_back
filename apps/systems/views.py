import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone

from apps.systems.models import System
from apps.systems.serializers import SystemSerializer

class SystemAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un sistema
      system = get_object_or_404(System, pk=pk)
      serializer = SystemSerializer(system)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de sistemas
    systems = System.objects.all()
    serializer = SystemSerializer(systems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nuevo sistema
    serializer = SystemSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    system = get_object_or_404(System, pk=pk)
    serializer = SystemSerializer(system, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    system = get_object_or_404(System, pk=pk)
    serializer = SystemSerializer(system, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    # Eliminación de sistema (no hay soft delete en este modelo)
    system = get_object_or_404(System, pk=pk)
    
    # Verificar si hay claves asociadas antes de eliminar
    if system.keys.exists():
      return Response(
        {'error': 'No se puede eliminar el sistema porque tiene claves asociadas'},
        status=status.HTTP_400_BAD_REQUEST
      )
        
    system.delete()
    return Response(
      {'message': 'Sistema eliminado exitosamente'},
      status=status.HTTP_204_NO_CONTENT
    )
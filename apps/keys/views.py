import traceback
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.utils import timezone
from apps.keys.models import Key
from apps.keys.serializers import KeySerializer

class KeyAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de una clave
      key = get_object_or_404(Key, pk=pk)
      serializer = KeySerializer(key)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de claves    
    keys = Key.objects.all()
    serializer = KeySerializer(keys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    # Creación de nueva clave
    serializer = KeySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk, format=None):
    # Actualización completa
    key = get_object_or_404(Key, pk=pk)
    serializer = KeySerializer(key, data=request.data)
    if serializer.is_valid():
      serializer.save(updated_by=request.user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def patch(self, request, pk, format=None):
    # Actualización parcial
    key = get_object_or_404(Key, pk=pk)
    serializer = KeySerializer(key, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save(updated_by=request.user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    # Eliminación de clave (no hay soft delete en este modelo)
    key = get_object_or_404(Key, pk=pk)
    key.delete()
    return Response(
      {'message': 'Clave eliminada exitosamente'},
      status=status.HTTP_204_NO_CONTENT
    )

class KeyBySystemAPIView(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request, system_id, format=None):
    # Obtener todas las claves de un sistema específico
    keys = Key.objects.filter(system_id=system_id)
    serializer = KeySerializer(keys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class KeyByConfigKeyAPIView(APIView):
  permission_classes = [IsAuthenticated]
  
  def get(self, request, config_key, format=None):
    # Obtener clave por config_key (útil para búsquedas)
    key = get_object_or_404(Key, config_key=config_key)
    serializer = KeySerializer(key)
    return Response(serializer.data, status=status.HTTP_200_OK)
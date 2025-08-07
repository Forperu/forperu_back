import traceback
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
  ListCreateAPIView,
  RetrieveUpdateDestroyAPIView
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserPublicSerializer

User = get_user_model()

class UserAPIView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser, FormParser, MultiPartParser]

  def get(self, request, pk=None, format=None):
    if pk:
      # Detalle de un usuario
      user = get_object_or_404(User, pk=pk, deleted_at__isnull=True)
      serializer = UserSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)

    # Listado de usuarios
    users = User.objects.filter(deleted_at__isnull=True)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request, format=None):
    # Usamos UserCreateSerializer para la creación que maneja mejor las contraseñas
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      # Devolvemos los datos con el UserSerializer para incluir las relaciones
      response_serializer = UserSerializer(user)
      return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def put(self, request, pk, format=None):
    # Actualización completa
    user = get_object_or_404(User, pk=pk, deleted_at__isnull=True)
    serializer = UserUpdateSerializer(user, data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      response_serializer = UserSerializer(user)
      return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request, pk, format=None):
    user = get_object_or_404(User, pk=pk, deleted_at__isnull=True)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
      # Manejo especial para la contraseña si viene en el PATCH
      if 'password' in request.data:
        user.set_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)  # Volvemos a serializar
        return Response(serializer.data, status=status.HTTP_200_OK)
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request, pk=None, format=None):
    if pk:
      # Eliminación individual (soft delete)
      user = get_object_or_404(User, pk=pk, deleted_at__isnull=True)
      user.deleted_at = timezone.now()
      user.save()
      return Response(
        {'message': 'User deleted successfully'}, 
        status=status.HTTP_204_NO_CONTENT
      )
    
    # Eliminación múltiple (opcional)
    return self._delete_multiple(request)
  
  def _delete_multiple(self, request):
    try:
      user_ids = request.data if isinstance(request.data, list) else request.data.get('ids', [])

      if not user_ids:
        return Response(
          {'error': 'No se proporcionaron IDs de usuarios'},
          status=status.HTTP_400_BAD_REQUEST
        )

      try:
        user_ids = [int(id) for id in user_ids]
      except (ValueError, TypeError):
        return Response(
          {'error': 'IDs de usuarios no válidos'},
          status=status.HTTP_400_BAD_REQUEST
        )

      existing_users = User.objects.filter(
        id__in=user_ids,
        deleted_at__isnull=True
      )

      if existing_users.count() != len(user_ids):
        return Response(
          {'error': 'Algunos IDs no existen o ya fueron eliminados'},
          status=status.HTTP_400_BAD_REQUEST
        )

      updated = existing_users.update(
        deleted_at=timezone.now(),
        updated_by=request.user
      )

      return Response({
        'message': f'{updated} usuarios eliminados exitosamente',
        'deleted_count': updated
      }, status=status.HTTP_200_OK)

    except Exception as e:
      traceback.print_exc()
      return Response(
        {'error': f'Error al eliminar usuarios: {str(e)}'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
  
class UserListCreateView(ListCreateAPIView):
  queryset = User.objects.filter(deleted_at__isnull=True)
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    instance = serializer.save()
    instance.set_password(self.request.data.get('password'))
    instance.save()

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
      return Response(
        {"error": "Email and password are required."},
        status=status.HTTP_400_BAD_REQUEST
      )

    try:
      user = User.objects.get(email=email)
      if not user.check_password(password):
        return Response(
          {"error": "Invalid credentials."},
          status=status.HTTP_401_UNAUTHORIZED
        )

      if not user.status:
        return Response(
          {"error": "User account is disabled."},
          status=status.HTTP_403_FORBIDDEN
        )

      refresh = RefreshToken.for_user(user)
      serializer = UserSerializer(user, context={'request': request})
      
      return Response({
        'user': serializer.data,
        'access_token': str(refresh.access_token)
      })

    except User.DoesNotExist:
      return Response(
        {"error": "User not found."},
        status=status.HTTP_404_NOT_FOUND
      )

class TokenLoginView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user
    
    if not user.status:
      return Response(
        {"error": "User account is disabled."},
        status=status.HTTP_403_FORBIDDEN
      )

    serializer = UserSerializer(user)
    return Response(serializer.data)
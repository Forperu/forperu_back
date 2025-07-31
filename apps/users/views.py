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

from .serializers import UserSerializer, UserPublicSerializer

User = get_user_model()

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

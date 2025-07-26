from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    qr_code = serializers.URLField(source="get_qr_code")
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = "__all__"

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'username',
            'slug',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'company_id'
        ]
        read_only_fields = ('id', 'slug')

class UserListSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'username',
            'slug',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'company_id'
        ]
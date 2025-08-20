from rest_framework import serializers
from apps.systems.models import System

class SystemSerializer(serializers.ModelSerializer):
  class Meta:
    model = System
    fields = [
      'id',
      'name',
      'description',
      'created_at',
      'updated_at'
    ]
    read_only_fields = ['created_at', 'updated_at']
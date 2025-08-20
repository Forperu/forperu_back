from rest_framework import serializers
from apps.keys.models import Key
from apps.systems.serializers import SystemSerializer

class KeySerializer(serializers.ModelSerializer):
  system = serializers.SerializerMethodField()
  system_id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = Key
    fields = [
      'id',
      'system',
      'system_id',
      'name',
      'description',
      'config_key',
      'config_value',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at'
    ]

  def get_system(self, obj):
    if obj.system:
      SystemSerializer.Meta.model = obj.system.__class__
      return SystemSerializer(obj.system).data
    return None
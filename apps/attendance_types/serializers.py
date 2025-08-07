from rest_framework import serializers
from apps.attendance_types.models import AttendanceType

class AttendanceTypeSerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()
  
  class Meta:
    model = AttendanceType
    fields = [
      'id',
      'name',
      'code',
      'description',
      'status',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
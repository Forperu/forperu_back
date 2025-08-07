from rest_framework import serializers
from apps.work_schedules.models import WorkSchedule

class WorkScheduleSerializer(serializers.ModelSerializer):
  is_default = serializers.IntegerField()
  status = serializers.IntegerField()
  
  class Meta:
    model = WorkSchedule
    fields = [
      'id',
      'name',
      'description',
      'status',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
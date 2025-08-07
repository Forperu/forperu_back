from rest_framework import serializers
from .models import ScheduleDetail
from apps.work_schedules.serializers import WorkScheduleSerializer

class ScheduleDetailSerializer(serializers.ModelSerializer):
  schedule = serializers.SerializerMethodField()
  schedule_id = serializers.IntegerField()
  is_working_day = serializers.BooleanField()
  
  class Meta:
    model = ScheduleDetail
    fields = [
      'id',
      'schedule_id',
      'schedule',
      'day_of_week',
      'start_time',
      'end_time',
      'is_working_day',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_schedule(self, obj):
    if obj.schedule:
      WorkScheduleSerializer.Meta.model = obj.schedule.__class__
      return WorkScheduleSerializer(obj.schedule).data
    return None
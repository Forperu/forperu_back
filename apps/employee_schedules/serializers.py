from rest_framework import serializers
from .models import EmployeeSchedule
from apps.employees.serializers import EmployeeSerializer
from apps.work_schedules.serializers import WorkScheduleSerializer

class EmployeeScheduleSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  schedule = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  schedule_id = serializers.IntegerField()
  
  class Meta:
    model = EmployeeSchedule
    fields = [
      'id',
      'employee_id',
      'employee',
      'schedule_id',
      'schedule',
      'effective_date',
      'end_date',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
  
  def get_schedule(self, obj):
    if obj.schedule:
      WorkScheduleSerializer.Meta.model = obj.schedule.__class__
      return WorkScheduleSerializer(obj.schedule).data
    return None
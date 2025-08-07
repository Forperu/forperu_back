from rest_framework import serializers
from .models import OvertimeRequest
from apps.employees.serializers import EmployeeSerializer

class OvertimeRequestSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  
  class Meta:
    model = OvertimeRequest
    fields = [
      'id',
      'employee_id',
      'employee',
      'date',
      'start_time',
      'end_time',
      'hours',
      'reason',
      'status',
      'approved_by',
      'approved_at',
      'rejection_reason',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
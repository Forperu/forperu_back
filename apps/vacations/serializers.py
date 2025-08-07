from rest_framework import serializers
from .models import Vacation
from apps.employees.serializers import EmployeeSerializer

class VacationSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  
  class Meta:
    model = Vacation
    fields = [
      'id',
      'employee_id',
      'employee',
      'start_date',
      'end_date',
      'days_taken',
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
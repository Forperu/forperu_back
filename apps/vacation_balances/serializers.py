from rest_framework import serializers
from .models import VacationBalance
from apps.employees.serializers import EmployeeSerializer

class VacationBalanceSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  
  class Meta:
    model = VacationBalance
    fields = [
      'id',
      'employee_id',
      'employee',
      'year',
      'total_days',
      'days_taken',
      'days_remaining',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
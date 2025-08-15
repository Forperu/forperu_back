from rest_framework import serializers
from .models import EmployeeIncident
from apps.employees.serializers import EmployeeSerializer

class EmployeeIncidentSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  
  class Meta:
    model = EmployeeIncident
    fields = [
      'id',
      'employee_id',
      'employee',
      'incident_type',
      'incident_date',
      'observation',
      'discount',
      'total_to_pay',
      'reported_by',
      'status',
      'resolved_at',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
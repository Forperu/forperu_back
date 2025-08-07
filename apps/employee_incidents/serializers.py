from rest_framework import serializers
from .models import EmployeeIncident
from apps.employees.serializers import EmployeeSerializer

class EmployeeIncidentSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  reported_by = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  reported_by_id = serializers.IntegerField()
  
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
      'reported_by_id',
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
  
  def get_reported_by(self, obj):
    if obj.reported_by:
      EmployeeSerializer.Meta.model = obj.reported_by.__class__
      return EmployeeSerializer(obj.reported_by).data
    return None
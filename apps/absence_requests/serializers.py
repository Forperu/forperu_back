from rest_framework import serializers
from .models import AbsenceRequest
from apps.employees.serializers import EmployeeSerializer
from apps.absence_types.serializers import AbsenceTypeSerializer

class AbsenceRequestSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  absence_type = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  absence_type_id = serializers.IntegerField()
  
  class Meta:
    model = AbsenceRequest
    fields = [
      'id',
      'employee_id',
      'employee',
      'absence_type_id',
      'absence_type',
      'start_date',
      'end_date',
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
  
  def get_absence_type(self, obj):
    if obj.absence_type:
      AbsenceTypeSerializer.Meta.model = obj.absence_type.__class__
      return AbsenceTypeSerializer(obj.absence_type).data
    return None
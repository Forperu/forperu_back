from rest_framework import serializers
from .models import Attendance
from apps.employees.serializers import EmployeeSerializer
from apps.attendance_types.serializers import AttendanceTypeSerializer

class AttendanceSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  attendance_type = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  attendance_type_id = serializers.IntegerField()
  
  class Meta:
    model = Attendance
    fields = [
      'id',
      'employee_id',
      'employee',
      'attendance_type_id',
      'attendance_type',
      'date',
      'check_in',
      'check_out',
      'worked_hours',
      'late_minutes',
      'early_departure_minutes',
      'notes',
      'status',
      'approved_by',
      'approved_at',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
  
  def get_attendance_type(self, obj):
    if obj.attendance_type:
      AttendanceTypeSerializer.Meta.model = obj.attendance_type.__class__
      return AttendanceTypeSerializer(obj.attendance_type).data
    return None
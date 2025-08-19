from rest_framework import serializers
from .models import Attendance
from apps.employees.serializers import EmployeeSerializer
from apps.attendance_types.serializers import AttendanceTypeSerializer

class AttendanceSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  
  class Meta:
    model = Attendance
    fields = '__all__'
    read_only_fields = ('updated_at', 'created_at', 'deleted_at')
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
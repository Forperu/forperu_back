from rest_framework import serializers
from .models import Payroll
from apps.employees.serializers import EmployeeSerializer

class PayrollSerializer(serializers.ModelSerializer):
  created_by = serializers.SerializerMethodField()
  approved_by = serializers.SerializerMethodField()
  
  class Meta:
    model = Payroll
    fields = [
      'id',
      'reference',
      'period_start',
      'period_end',
      'payment_date',
      'status',
      'notes',
      'created_by',
      'approved_by',
      'approved_at',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_created_by(self, obj):
    if obj.created_by:
      EmployeeSerializer.Meta.model = obj.created_by.__class__
      return EmployeeSerializer(obj.created_by).data
    return None
  
  def get_approved_by(self, obj):
    if obj.approved_by:
      EmployeeSerializer.Meta.model = obj.approved_by.__class__
      return EmployeeSerializer(obj.approved_by).data
    return None
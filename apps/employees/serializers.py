from rest_framework import serializers
from apps.employees.models import Employee
from apps.job_positions.serializers import JobPositionSerializer
from apps.warehouses.serializers import WarehouseSerializer

class EmployeeSerializer(serializers.ModelSerializer):
  warehouse = serializers.SerializerMethodField()
  warehouse_id = serializers.IntegerField(required=False, allow_null=True)
  job_position = serializers.SerializerMethodField()
  job_position_id = serializers.IntegerField(required=False, allow_null=True)
  status = serializers.IntegerField()

  class Meta:
    model = Employee
    fields = '__all__'
    read_only_fields = ('updated_at', 'created_at', 'deleted_at')

  def get_warehouse(self, obj):
    if obj.warehouse:
      return WarehouseSerializer(obj.warehouse).data
    return None

  def get_job_position(self, obj):
    if obj.job_position:
      return JobPositionSerializer(obj.job_position).data
    return None
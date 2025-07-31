from rest_framework import serializers
from apps.warehouses.models import Warehouse
from apps.branch_offices.serializers import BranchOfficeSerializer

class WarehouseSerializer(serializers.ModelSerializer):
  branch_office = serializers.SerializerMethodField()

  class Meta:
    model = Warehouse
    fields = [
      'id',
      'company',
      'company_id',
      'branch_office',
      'branch_office_id',
      'name',
      'description',
      'address',
      'phone',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]

  def get_branch_office(self, obj):
    if obj.branch_office:
      BranchOfficeSerializer.Meta.model = obj.branch_office.__class__
      return BranchOfficeSerializer(obj.branch_office).data
    return None
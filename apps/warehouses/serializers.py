from rest_framework import serializers
from apps.warehouses.models import Warehouse
from apps.companies.serializers import CompanySerializer
from apps.branch_offices.serializers import BranchOfficeSerializer

class WarehouseSerializer(serializers.ModelSerializer):
  company = serializers.SerializerMethodField()
  company_id = serializers.IntegerField(required=False, allow_null=True)
  branch_office = serializers.SerializerMethodField()
  branch_office_id = serializers.IntegerField(required=False, allow_null=True)
  status = serializers.IntegerField()

  class Meta:
    model = Warehouse
    fields = [
      'id',
      'company',
      'company_id',
      'branch_office',
      'branch_office_id',
      'company_or_branch_office',
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

  def get_company(self, obj):
    if obj.company:
      CompanySerializer.Meta.model = obj.company.__class__
      return CompanySerializer(obj.company).data
    return None

  def get_branch_office(self, obj):
    if obj.branch_office:
      BranchOfficeSerializer.Meta.model = obj.branch_office.__class__
      return BranchOfficeSerializer(obj.branch_office).data
    return None
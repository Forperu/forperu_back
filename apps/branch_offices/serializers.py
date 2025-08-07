from rest_framework import serializers
from apps.branch_offices.models import BranchOffice
from apps.companies.serializers import CompanySerializer

class BranchOfficeSerializer(serializers.ModelSerializer):
  company = serializers.SerializerMethodField()
  company_id = serializers.IntegerField()
  status = serializers.IntegerField()

  class Meta:
    model = BranchOffice
    fields = [
      'id',
      'company',
      'company_id',
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
from rest_framework import serializers
from apps.companies.models import Company

class CompanySerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()
  
  class Meta:
    model = Company
    fields = [
      'id',
      'name',
      'logo',
      'ruc',
      'email',
      'phone',
      'web_site',
      'address',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
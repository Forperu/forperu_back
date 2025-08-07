from rest_framework import serializers
from apps.brands.models import Brand

class BrandSerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()
  
  class Meta:
    model = Brand
    fields = [
      'id',
      'name',
      'description',
      'logo_url',
      'website_url',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
from rest_framework import serializers
from apps.categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()
  
  class Meta:
    model = Category
    fields = [
      'id',
      'name',
      'description',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
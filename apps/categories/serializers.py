from rest_framework import serializers
from apps.categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()
  
  class Meta:
    model = Category
    fields = '__all__'
    read_only_fields = ('updated_at', 'created_at', 'deleted_at')
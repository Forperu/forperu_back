from rest_framework import serializers
from .models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
  recurring = serializers.BooleanField()
  status = serializers.BooleanField()
  
  class Meta:
    model = Holiday
    fields = [
      'id',
      'name',
      'description',
      'date',
      'recurring',
      'status',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
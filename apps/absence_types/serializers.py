from rest_framework import serializers
from .models import AbsenceType

class AbsenceTypeSerializer(serializers.ModelSerializer):
  requires_approval = serializers.BooleanField()
  is_paid = serializers.BooleanField()
  deducts_vacation = serializers.BooleanField()
  status = serializers.BooleanField()
  
  class Meta:
    model = AbsenceType
    fields = [
      'id',
      'name',
      'code',
      'description',
      'requires_approval',
      'is_paid',
      'deducts_vacation',
      'status',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
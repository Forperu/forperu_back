from rest_framework import serializers
from apps.customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()

  class Meta:
    model = Customer
    fields = [
      'id',
      'names',
      'surname',
      'second_surname',
      'company_name',
      'document_type',
      'document_number',
      'email',
      'phone',
      'address',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
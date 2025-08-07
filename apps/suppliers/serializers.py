from rest_framework import serializers
from apps.suppliers.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()

  class Meta:
    model = Supplier
    fields = [
      'id',
      'name',
      'ruc',
      'email',
      'phone',
      'address',
      'web_site',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
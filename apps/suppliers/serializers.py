from rest_framework import serializers
from apps.suppliers.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):

  class Meta:
    model = Supplier
    fields = [
      'id',
      'name',
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
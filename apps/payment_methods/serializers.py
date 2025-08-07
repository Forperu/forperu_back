from rest_framework import serializers
from apps.payment_methods.models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()

  class Meta:
    model = PaymentMethod
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
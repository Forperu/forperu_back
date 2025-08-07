from rest_framework import serializers
from apps.currencies.models import Currency

class CurrencySerializer(serializers.ModelSerializer):
  status = serializers.IntegerField()
  
  class Meta:
    model = Currency
    fields = [
      'id',
      'name',
      'description',
      'code',
      'symbol',
      'status',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
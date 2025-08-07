from rest_framework import serializers
from apps.currencies.serializers import CurrencySerializer
from apps.exchange_rates.models import ExchangeRate

class ExchangeRateSerializer(serializers.ModelSerializer):
  base_currency = CurrencySerializer(read_only=True)
  target_currency = CurrencySerializer(read_only=True)
  base_currency_id = serializers.IntegerField()
  target_currency_id = serializers.IntegerField()

  class Meta:
    model = ExchangeRate
    fields = [
      'id',
      'base_currency',
      'base_currency_id',
      'target_currency',
      'target_currency_id',
      'exchange_rate',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]

    def get_base_currency(self, obj):
      if obj.base_currency:
        return CurrencySerializer(obj.base_currency).data
      return None

    def get_target_currency(self, obj):
      if obj.target_currency:
        return CurrencySerializer(obj.target_currency).data
      return None
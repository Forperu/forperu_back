from rest_framework import serializers
from apps.exchange_rates.models import ExchangeRate

class ExchangeRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = ExchangeRate
    fields = ['id', 'base_currency', 'target_currency', 'exchange_rate', 'created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at']
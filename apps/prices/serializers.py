from rest_framework import serializers
from apps.prices.models import Price
from apps.products.serializers import ProductSerializer

class PriceSerializer(serializers.ModelSerializer):
  product = serializers.SerializerMethodField()
  product_id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = Price
    fields = [
      'id',
      'product',
      'product_id',
      'cost',
      'price_cf',
      'price_sf',
      'price_box',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]

  def get_product(self, obj):
    if obj.product:
      ProductSerializer.Meta.model = obj.product.__class__
      return ProductSerializer(obj.product).data
    return None
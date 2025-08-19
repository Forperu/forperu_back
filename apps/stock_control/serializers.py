from rest_framework import serializers
from apps.stock_control.models import StockControl
from apps.warehouses.serializers import WarehouseSerializer
from apps.products.serializers import ProductSerializer

class StockControlSerializer(serializers.ModelSerializer):
  warehouse = serializers.SerializerMethodField()
  warehouse_id = serializers.IntegerField(required=False, allow_null=True)
  product = serializers.SerializerMethodField()
  product_id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = StockControl
    fields = '__all__'
    read_only_fields = ('updated_at', 'created_at', 'deleted_at')

  def get_warehouse(self, obj):
    if obj.warehouse:
      WarehouseSerializer.Meta.model = obj.warehouse.__class__
      return WarehouseSerializer(obj.warehouse).data
    return None

  def get_product(self, obj):
    if obj.product:
      ProductSerializer.Meta.model = obj.product.__class__
      return ProductSerializer(obj.product).data
    return None
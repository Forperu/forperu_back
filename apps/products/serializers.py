from rest_framework import serializers
from apps.brands.serializers import BrandSerializer
from apps.products.models import Product
from apps.units_of_measurement.serializers import UnitOfMeasurementSerializer

class ProductSerializer(serializers.ModelSerializer):
  brand = serializers.SerializerMethodField()
  brand_id = serializers.IntegerField(required=False, allow_null=True)
  unit_of_measurement = serializers.SerializerMethodField()
  unit_of_measurement_id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = Product
    fields = '__all__'
    read_only_fields = ('updated_at', 'created_at', 'deleted_at')

  def get_brand(self, obj):
    if obj.brand:
      BrandSerializer.Meta.model = obj.brand.__class__
      return BrandSerializer(obj.brand).data
    return None

  def get_unit_of_measurement(self, obj):
    if obj.unit_of_measurement:
      UnitOfMeasurementSerializer.Meta.model = obj.unit_of_measurement.__class__
      return UnitOfMeasurementSerializer(obj.unit_of_measurement).data
    return None
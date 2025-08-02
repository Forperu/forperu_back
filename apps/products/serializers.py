from rest_framework import serializers
from apps.brands.serializers import BrandSerializer
from apps.products.models import Product
from apps.units_of_measurement.serializers import UnitOfMeasurementSerializer

class ProductSerializer(serializers.ModelSerializer):
  brand = serializers.SerializerMethodField()
  unit_of_measurement = serializers.SerializerMethodField()

  class Meta:
    model = Product
    fields = [
      'id',
      'name',
      'brand_id',
      'brand',
      'unit_of_measurement_id',
      'unit_of_measurement',
      'handle',
      'description',
      'tags',
      'featured_image',
      'images',
      'prices_cf',
      'prices_sf',
      'prices_box',
      'featured_pcf',
      'featured_psf',
      'featured_pbox',
      'quantity_in_box',
      'cost',
      'tax_rate',
      'quantity',
      'sku',
      'width',
      'height',
      'depth',
      'liters',
      'weight',
      'barcode',
      'rating',
      'extra_shipping_fee',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]

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
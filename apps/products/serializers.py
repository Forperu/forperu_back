from rest_framework import serializers
from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = [
      'id', 'name', 'brand', 'unit_of_measurement', 'handle','description', 'tags', 'featured_image', 'images',
      'prices_cf', 'prices_sf', 'prices_box', 'featured_pcf', 'featured_psf', 'featured_pbox',
      'quantity_in_box', 'cost', 'tax_rate', 'quantity', 'sku',
      'width', 'height', 'depth', 'liters', 'weight', 'barcode', 'rating', 'extra_shipping_fee',
      'status', 'created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at']
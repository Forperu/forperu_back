from rest_framework import serializers
from apps.brands.serializers import BrandSerializer
from apps.categories.serializers import CategorySerializer
from apps.products.models import Product, ProductCategory
from apps.stock_control.models import StockControl
from apps.units_of_measurement.serializers import UnitOfMeasurementSerializer
from django.db.models import Sum

class ProductCategorySerializer(serializers.ModelSerializer):
  category = serializers.SerializerMethodField()
  category_id = serializers.IntegerField(write_only=True)

  class Meta:
    model = ProductCategory
    fields = ['id', 'category', 'category_id', 'product']

  def get_category(self, obj):
    if obj.category:
      CategorySerializer.Meta.model = obj.category.__class__
      return CategorySerializer(obj.category).data
    return None
    
class ProductSerializer(serializers.ModelSerializer):
  brand = serializers.SerializerMethodField()
  unit_of_measurement = serializers.SerializerMethodField()
  categories = serializers.SerializerMethodField()
  category_ids = serializers.ListField(
    child=serializers.IntegerField(),
    write_only=True,
    required=False
  )
  stock = serializers.SerializerMethodField()
  booking = serializers.SerializerMethodField()

  class Meta:
    model = Product
    fields = [
      'id',
      'name',
      'brand_id',
      'brand',
      'categories',
      'category_ids',
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
      'stock',
      'booking',
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
  
  def get_categories(self, obj):
    categories = obj.categories.all()
    return CategorySerializer(categories, many=True).data

  def create(self, validated_data):
    category_ids = validated_data.pop('category_ids', [])
    product = super().create(validated_data)
    
    if category_ids:
      product.categories.set(category_ids)
    
    return product

  def update(self, instance, validated_data):
    category_ids = validated_data.pop('category_ids', None)
    product = super().update(instance, validated_data)
    
    if category_ids is not None:
      product.categories.set(category_ids)
    
    return product
  
  def get_stock(self, obj):
    stock = StockControl.objects.filter(
      product=obj,
      deleted_at__isnull=True
    ).aggregate(total_stock=Sum('current_stock'))['total_stock'] or 0
    return stock
  
  def get_booking(self, obj):
    booking = StockControl.objects.filter(
      product=obj,
      deleted_at__isnull=True
    ).aggregate(total_booking=Sum('current_booking'))['total_booking'] or 0
    return booking
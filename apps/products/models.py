from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from apps.brands.models import Brand
from apps.categories.models import Category
from apps.units_of_measurement.models import UnitOfMeasurement

class ProductManager(models.Manager):
  def with_stock(self):
    return self.get_queryset().annotate(
      total_stock=Coalesce(Sum('stock_controls__current_stock'), 0)
    )
  
  def with_booking(self):
    return self.get_queryset().annotate(
      total_booking=Coalesce(Sum('stock_controls__current_booking'), Value(0))
    )

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=255)
  brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, db_column='brand_id', null=True, blank=True, related_name='products')
  unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.SET_NULL, db_column='unit_of_measurement_id', null=True, blank=True, related_name='products')
  handle = models.TextField(max_length=255, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  tags = models.JSONField(default=dict, blank=True, null=True)
  featured_image = models.TextField(max_length=10, null=True, blank=True)
  images = models.JSONField(default=dict, blank=True, null=True)
  prices_cf = models.JSONField(default=dict, blank=True, null=True)
  prices_sf = models.JSONField(default=dict, blank=True, null=True)
  prices_box = models.JSONField(default=dict, blank=True, null=True)
  featured_pcf = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
  featured_psf = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
  featured_pbox = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
  quantity_in_box = models.SmallIntegerField(null=True, blank=True)
  cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
  tax_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
  quantity = models.DecimalField(max_digits=14, decimal_places=2, default=0, null=True, blank=True)
  sku = models.CharField(max_length=50, null=True, blank=True)
  width = models.DecimalField(max_digits=14, decimal_places=2, default=0, null=True, blank=True)
  height = models.DecimalField(max_digits=14, decimal_places=2, default=0, null=True, blank=True)
  depth = models.DecimalField(max_digits=14, decimal_places=2, default=0, null=True, blank=True)
  liters = models.DecimalField(max_digits=14, decimal_places=2, default=0, null=True, blank=True)
  weight = models.DecimalField(max_digits=14, decimal_places=2, default=0, null=True, blank=True)
  barcode = models.CharField(max_length=100, null=True, blank=True)
  rating = models.DecimalField(max_digits=4, decimal_places=2, default=0, null=True, blank=True)
  extra_shipping_fee = models.DecimalField(max_digits=14, decimal_places=2, default=0, null=True, blank=True)
  status = models.BooleanField(default=1)
  created_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.CASCADE,
    db_column='created_by',
    related_name='created_%(class)s'
  )
  updated_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='updated_by',
    related_name='updated_%(class)s'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  categories = models.ManyToManyField(
    Category,
    through='ProductCategory',
    related_name='products'
  )

  objects = ProductManager()

  class Meta:
    managed = True
    db_table = 'products'

class ProductCategory(models.Model):
  product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    related_name='product_categories'
  )
  category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    related_name='product_categories'
  )
  
  class Meta:
    db_table = 'product_categories'
    unique_together = ('product', 'category')
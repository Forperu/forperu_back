from django.db import models

from apps.brands.models import Brand
from apps.units_of_measurement.models import UnitOfMeasurement

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=255)
  brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, db_column='brand_id', null=True, blank=True, related_name='products')
  unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.SET_NULL, db_column='unit_of_measurement_id', null=True, blank=True, related_name='products')
  handle = models.TextField(max_length=255, null=True, blank=True)
  description = models.TextField()
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
  status = models.BooleanField(default=True)
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

  class Meta:
    managed = True
    db_table = 'products'
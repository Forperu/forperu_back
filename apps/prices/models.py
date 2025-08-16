from django.db import models

from apps.products.models import Product

# Create your models here.
class Price(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id', null=True, blank=True)
  cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
  price_cf = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
  price_sf = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
  price_box = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
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
    db_table = 'prices'
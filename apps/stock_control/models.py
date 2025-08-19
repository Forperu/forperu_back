from django.db import models
from apps.warehouses.models import Warehouse
from apps.products.models import Product

# Create your models here.
class StockControl(models.Model):
  warehouse = models.ForeignKey(
    Warehouse,
    on_delete=models.CASCADE,
    db_column='warehouse_id',
    related_name='stock_controls'
  )
  product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    db_column='product_id',
    related_name='stock_controls'
  )
  current_stock = models.PositiveIntegerField(default=0)
  current_booking = models.PositiveIntegerField(default=0)
  min_stock = models.PositiveIntegerField(null=True, blank=True)
  max_stock = models.PositiveIntegerField(null=True, blank=True)
  created_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='created_by',
    related_name='created_stock_controls'
  )
  updated_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='updated_by',
    related_name='updated_stock_controls'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'stock_control'
    constraints = [
      models.CheckConstraint(check=models.Q(current_stock__gte=0), name='chk_current_stock_gte_0'),
      models.CheckConstraint(check=models.Q(current_booking__gte=0), name='chk_current_booking_gte_0'),
      models.CheckConstraint(check=models.Q(max_stock__gt=models.F('min_stock')), name='chk_max_stock_gt_min_stock'),
    ]

  def __str__(self):
    return f"{self.product.name} - {self.warehouse.name}"
from django.db import models
from apps.products.models import Product
from apps.warehouses.models import Warehouse

# Create your models here.
class InventoryMovement(models.Model):
  MOVEMENT_TYPES = [
    ('entry', 'Entry'),
    ('exit', 'Exit'),
    ('adjustment', 'Adjustment'),
  ]

  warehouse = models.ForeignKey(
    Warehouse,
    on_delete=models.CASCADE,
    db_column='warehouse_id',
    related_name='inventory_movements'
  )
  product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    db_column='product_id',
    related_name='inventory_movements'
  )
  movement_type = models.CharField(max_length=50, choices=MOVEMENT_TYPES, null=True, blank=True)
  quantity = models.PositiveIntegerField()
  reference = models.CharField(max_length=8, null=True, blank=True)
  user = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='user_id',
    related_name='inventory_movements'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'inventory_movements'
    constraints = [
      models.CheckConstraint(check=models.Q(quantity__gt=0), name='chk_quantity_gt_0'),
    ]

  def __str__(self):
    return f"{self.movement_type} - {self.product.name} ({self.quantity})"
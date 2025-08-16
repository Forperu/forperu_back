from django.db import models

from apps.currencies.models import Currency
from apps.customers.models import Customer
from apps.products.models import Product
from apps.warehouses.models import Warehouse

class Quote(models.Model):
  reference = models.CharField(max_length=8)
  warehouse = models.ForeignKey(
    Warehouse,
    on_delete=models.SET_NULL,
    db_column='warehouse_id',
    null=True,
    blank=True,
    related_name='quotes'
  )
  customer = models.ForeignKey(
    Customer,
    on_delete=models.CASCADE,
    db_column='customer_id',
    related_name='quotes'
  )
  currency = models.ForeignKey(
    Currency,
    on_delete=models.CASCADE,
    db_column='currency_id',
    related_name='quotes'
  )
  user = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    db_column='user_id',
    null=True,
    blank=True,
    related_name='quotes_created'
  )
  issue_date = models.DateTimeField(auto_now_add=True)
  exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)
  expiration_date = models.DateTimeField(null=True, blank=True)

  approved_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    db_column='approved_by',
    null=True,
    blank=True,
    related_name='quotes_approved'
  )
  approved_at = models.DateTimeField(null=True, blank=True)

  canceled_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    db_column='canceled_by',
    null=True,
    blank=True,
    related_name='quotes_canceled'
  )
  canceled_at = models.DateTimeField(null=True, blank=True)

  discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
  subtotal = models.DecimalField(max_digits=14, decimal_places=2)
  total = models.DecimalField(max_digits=14, decimal_places=2)

  QUOTE_STATUS_CHOICES = [
    ('issued', 'Issued'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
  ]
  quote_status = models.CharField(max_length=20, choices=QUOTE_STATUS_CHOICES, default='issued')

  migrate_quote = models.BooleanField(default=0)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'quotes'

  def __str__(self):
    return f"{self.reference} - {self.customer}"


class QuoteDetail(models.Model):
  product_name = models.CharField(max_length=150, null=True, blank=True)
  quote = models.ForeignKey(
    Quote,
    on_delete=models.CASCADE,
    db_column='quote_id',
    related_name='details'
  )
  product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    db_column='product_id',
    related_name='quote_details'
  )
  quantity = models.DecimalField(max_digits=14, decimal_places=2)
  price = models.DecimalField(max_digits=14, decimal_places=2)
  discount_method = models.BooleanField(default=1)  # True = porcentaje, False = monto
  discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
  subtotal = models.DecimalField(max_digits=14, decimal_places=2)
  total = models.DecimalField(max_digits=14, decimal_places=2)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
      managed = True
      db_table = 'quote_details'

  def __str__(self):
    return f"{self.product_name or self.product.name} - {self.quantity}"
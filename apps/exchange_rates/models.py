from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
  base_currency = models.ForeignKey(
    'currencies.Currency',
    on_delete=models.CASCADE,
    db_column='base_currency_id',
    related_name='base_currency_rates'  # Nombre único para relación inversa
  )
  target_currency = models.ForeignKey(
    'currencies.Currency',
    on_delete=models.CASCADE,
    db_column='target_currency_id',
    related_name='target_currency_rates'  # Nombre único para relación inversa
  )
  exchange_rate = models.DecimalField(max_digits=18, decimal_places=6)
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
    db_table = 'exchange_rates'
from django.db import models
from django.core.validators import MinValueValidator
from eth_typing import ValidationError

# Create your models here.
class Payroll(models.Model):
  DRAFT = 'draft'
  CALCULATED = 'calculated'
  APPROVED = 'approved'
  PAID = 'paid'
  CANCELED = 'canceled'
  
  STATUS_CHOICES = [
    (DRAFT, 'Draft'),
    (CALCULATED, 'Calculated'),
    (APPROVED, 'Approved'),
    (PAID, 'Paid'),
    (CANCELED, 'Canceled'),
  ]
  
  reference = models.CharField(max_length=20, unique=True)
  period_start = models.DateField()
  period_end = models.DateField(validators=[MinValueValidator('period_start')])
  payment_date = models.DateField(validators=[MinValueValidator('period_end')])
  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default=DRAFT
  )
  notes = models.TextField(null=True, blank=True)
  created_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='created_by',
    related_name='created_payrolls'
  )
  approved_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='approved_by',
    related_name='approved_payrolls'
  )
  approved_at = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'payrolls'
    verbose_name = 'Payroll'
    verbose_name_plural = 'Payrolls'

  def clean(self):
    if self.period_end < self.period_start:
      raise ValidationError("Period end must be greater than or equal to period start")
    if self.payment_date < self.period_end:
      raise ValidationError("Payment date must be greater than or equal to period end")

  def __str__(self):
    return f"{self.reference} - {self.period_start} to {self.period_end}"
from django.db import models
from eth_typing import ValidationError
from apps.employees.models import Employee

# Create your models here.
class EmployeeBenefit(models.Model):
  employee = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    db_column='employee_id'
  )
  benefit_type = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
  start_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)
  status = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'employee_benefits'
    verbose_name = 'Employee Benefit'
    verbose_name_plural = 'Employee Benefits'

  def clean(self):
    if self.end_date and self.end_date < self.start_date:
      raise ValidationError("End date must be greater than or equal to start date")

  def __str__(self):
    return f"{self.employee} - {self.benefit_type} (${self.amount})"
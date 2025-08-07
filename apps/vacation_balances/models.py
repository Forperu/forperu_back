from django.db import models

from apps.employees.models import Employee

# Create your models here.
class VacationBalance(models.Model):
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')
  year = models.SmallIntegerField()
  total_days = models.SmallIntegerField()
  days_taken = models.SmallIntegerField(default=0)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'vacation_balances'

  @property
  def days_remaining(self):
    return self.total_days - self.days_taken
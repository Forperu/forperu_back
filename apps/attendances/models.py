from django.db import models

from apps.attendance_types.models import AttendanceType
from apps.employees.models import Employee

# Create your models here.
class Attendance(models.Model):
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')
  date = models.DateField()
  check_in = models.TimeField(null=True, blank=True)
  check_out = models.TimeField(null=True, blank=True)
  time_worked = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
  late_minutes = models.SmallIntegerField(null=True, blank=True, default=0)
  early_departure_minutes = models.SmallIntegerField(null=True, blank=True, default=0)
  observation = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'attendances'
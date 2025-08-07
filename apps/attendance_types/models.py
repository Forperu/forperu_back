from django.db import models

from apps.employees.models import Employee

# Create your models here.
class AttendanceType(models.Model):
  name = models.CharField(max_length=50)
  code = models.CharField(max_length=10)
  description = models.TextField(null=True, blank=True)
  status = models.BooleanField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'attendance_types'
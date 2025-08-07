from django.db import models

from apps.attendance_types.models import AttendanceType
from apps.employees.models import Employee

# Create your models here.
class Attendance(models.Model):
  PENDING = 'pending'
  APPROVED = 'approved'
  REJECTED = 'rejected'
  
  STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
  ]
  
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')
  attendance_type = models.ForeignKey(AttendanceType, on_delete=models.CASCADE, db_column='attendance_type_id')
  date = models.DateField()
  check_in = models.DateTimeField(null=True, blank=True)
  check_out = models.DateTimeField(null=True, blank=True)
  worked_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
  late_minutes = models.SmallIntegerField(null=True, blank=True, default=0)
  early_departure_minutes = models.SmallIntegerField(null=True, blank=True, default=0)
  notes = models.TextField(null=True, blank=True)
  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default=PENDING
  )
  approved_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='approved_by',
    related_name='approved_%(class)s'
  )
  approved_at = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'attendances'
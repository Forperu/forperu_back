from django.db import models
from django.core.validators import MinValueValidator
from eth_typing import ValidationError
from apps.absence_types.models import AbsenceType
from apps.employees.models import Employee

# Create your models here.
class AbsenceRequest(models.Model):
  PENDING = 'pending'
  APPROVED = 'approved'
  REJECTED = 'rejected'
  CANCELED = 'canceled'
  
  STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (REJECTED, 'Rejected'),
    (CANCELED, 'Canceled'),
  ]
  
  employee = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    db_column='employee_id'
  )
  absence_type = models.ForeignKey(
    AbsenceType,
    on_delete=models.CASCADE,
    db_column='absence_type_id'
  )
  start_date = models.DateField()
  end_date = models.DateField(
    validators=[MinValueValidator('start_date')]
  )
  reason = models.TextField(null=True, blank=True)
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
    related_name='approved_absence_requests'
  )
  approved_at = models.DateTimeField(null=True, blank=True)
  rejection_reason = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
      managed = True
      db_table = 'absence_requests'

  def clean(self):
    if self.end_date < self.start_date:
      raise ValidationError("End date must be greater than or equal to start date")

  def __str__(self):
    return f"{self.employee} - {self.absence_type} ({self.start_date} to {self.end_date})"
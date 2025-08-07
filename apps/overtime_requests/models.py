from django.db import models
from django.db.models import F
from datetime import datetime
from apps.employees.models import Employee

# Create your models here.
class OvertimeRequest(models.Model):
  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('canceled', 'Canceled'),
  ]
  
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')
  date = models.DateField()
  start_time = models.TimeField()
  end_time = models.TimeField()
  reason = models.TextField()
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  approved_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='approved_by',
    related_name='approved_%(class)s'
  )
  approved_at = models.DateTimeField(null=True, blank=True)
  rejection_reason = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'overtime_requests'
    constraints = [
      models.CheckConstraint(
        check=models.Q(end_time__gt=F('start_time')),
        name='check_end_time_gt_start_time'
      ),
      models.CheckConstraint(
        check=models.Q(status__in=['pending', 'approved', 'rejected', 'canceled']),
        name='valid_status_check'
      )
    ]

  @property
  def hours(self):
    dummy_date = datetime.today().date()
    start = datetime.combine(dummy_date, self.start_time)
    end = datetime.combine(dummy_date, self.end_time)
    duration = end - start
    return round(duration.total_seconds() / 3600, 2)

  def __str__(self):
    return f"Overtime {self.date} - Employee {self.employee_id}"
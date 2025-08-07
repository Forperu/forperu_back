from django.db import models

from apps.employees.models import Employee

# Create your models here.
class EmployeeIncident(models.Model):
  OPEN = 'open'
  INVESTIGATING = 'investigating'
  RESOLVED = 'resolved'
  CLOSED = 'closed'
  
  STATUS_CHOICES = [
    (OPEN, 'Open'),
    (INVESTIGATING, 'Investigating'),
    (RESOLVED, 'Resolved'),
    (CLOSED, 'Closed'),
  ]
  
  employee = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    db_column='employee_id',
    related_name='incidents'
  )
  incident_type = models.CharField(max_length=50)
  incident_date = models.DateField()
  observation = models.TextField()
  discount = models.DecimalField(max_digits=14, decimal_places=2)
  total_to_pay = models.DecimalField(max_digits=14, decimal_places=2)
  reported_by = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    db_column='reported_by',
    related_name='reported_incidents'
  )
  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default=OPEN
  )
  resolved_at = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'employee_incidents'
    verbose_name = 'Employee Incident'
    verbose_name_plural = 'Employee Incidents'

  def __str__(self):
    return f"{self.incident_type} - {self.employee} on {self.incident_date}"
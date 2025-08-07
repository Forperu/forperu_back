from django.db import models
from django.db.models import F
from apps.employees.models import Employee
from apps.work_schedules.models import WorkSchedule

# Create your models here.
class EmployeeSchedule(models.Model):
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_id')
  schedule = models.ForeignKey(
    WorkSchedule,
    on_delete=models.CASCADE,
    related_name='employee_schedules'
  )
  effective_date = models.DateField()
  end_date = models.DateField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'employee_schedules'
    constraints = [
      models.CheckConstraint(
        check=(
          models.Q(end_date__isnull=True) |
          models.Q(end_date__gte=F('effective_date'))
        ),
        name='check_end_date_after_effective_date'
      )
    ]

  def __str__(self):
    return f"Employee {self.employee_id} - Schedule {self.schedule_id}"
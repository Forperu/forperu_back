from django.db import models
from django.db.models import F
from apps.work_schedules.models import WorkSchedule

# Create your models here.
class ScheduleDetail(models.Model):
  schedule = models.ForeignKey(
    WorkSchedule,
    on_delete=models.CASCADE, 
    related_name='details'
  )
  day_of_week = models.SmallIntegerField()  # 0=Domingo, 1=Lunes, ...
  start_time = models.TimeField()
  end_time = models.TimeField()
  is_working_day = models.BooleanField(default=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'schedule_details'
    constraints = [
      models.CheckConstraint(
        check=models.Q(day_of_week__gte=0, day_of_week__lte=6),
        name='day_of_week_valid_range'
      ),
      models.CheckConstraint(
        check=(
          models.Q(is_working_day=False) |
          models.Q(end_time__gt=F('start_time'))
        ),
        name='working_day_time_check'
      )
    ]

  def __str__(self):
    return f"{self.schedule.name} - Día {self.day_of_week}"
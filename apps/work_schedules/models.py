from django.db import models

# Create your models here.
class WorkSchedule(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  is_default = models.BooleanField(default=False)
  status = models.BooleanField(default=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'work_schedules'

  def __str__(self):
    return self.name
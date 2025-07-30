from django.db import models

# Create your models here.
class JobPosition(models.Model):
  work_area = models.ForeignKey('work_areas.WorkArea', on_delete=models.CASCADE, db_column='work_area_id')
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  status = models.BooleanField(default=True)
  created_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.CASCADE,
    db_column='created_by',
    related_name='created_%(class)s'
  )
  updated_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='updated_by',
    related_name='updated_%(class)s'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'job_positions'
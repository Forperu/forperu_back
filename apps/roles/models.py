from django.db import models
from django.utils import timezone

# Create your models here.
class Role(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'roles'
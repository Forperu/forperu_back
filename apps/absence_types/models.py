from django.db import models

# Create your models here.
class AbsenceType(models.Model):
  name = models.CharField(max_length=50)
  code = models.CharField(max_length=10)
  description = models.TextField(null=True, blank=True)
  requires_approval = models.BooleanField(default=True)
  is_paid = models.BooleanField(default=False)
  deducts_vacation = models.BooleanField(default=False)
  status = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'absence_types'

  def __str__(self):
    return f"{self.code} - {self.name}"
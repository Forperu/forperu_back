from django.db import models

# Create your models here.
class Holiday(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  date = models.DateField()
  recurring = models.BooleanField(default=False)
  status = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'holidays'

  def __str__(self):
    return f"{self.name} ({self.date})"
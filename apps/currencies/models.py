from django.db import models

# Create your models here.
class Currency(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  code = models.CharField(max_length=10, unique=True)
  symbol = models.CharField(max_length=10)
  status = models.BooleanField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'currencies'
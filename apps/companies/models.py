from django.db import models

# Create your models here.
class Company(models.Model):
  name = models.CharField(max_length=200)
  logo = models.CharField(max_length=150, null=True, blank=True)
  ruc = models.CharField(max_length=11)
  email = models.CharField(max_length=255, null=True, blank=True)
  phone = models.CharField(max_length=15, null=True, blank=True)
  web_site = models.CharField(max_length=100, null=True, blank=True)
  address = models.TextField()
  status = models.BooleanField(default=1)
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
    db_table = 'companies'
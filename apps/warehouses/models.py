from django.db import models

from apps.branch_offices.models import BranchOffice
from apps.companies.models import Company

# Create your models here.
class Warehouse(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id', null=True, blank=True)
  branch_office = models.ForeignKey(BranchOffice, on_delete=models.CASCADE, db_column='branch_office_id', null=True, blank=True)
  company_or_branch_office = models.BooleanField(default=1)
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  address = models.TextField(null=True, blank=True)
  phone = models.CharField(max_length=15, null=True, blank=True)
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
    db_table = 'warehouses'
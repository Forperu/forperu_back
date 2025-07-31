from django.db import models

# Create your models here.
class Customer(models.Model):
  names = models.CharField(max_length=150, null=True, blank=True)
  surname = models.CharField(max_length=50, null=True, blank=True)
  second_surname = models.CharField(max_length=50, null=True, blank=True)
  company_name = models.CharField(max_length=100, null=True, blank=True)
  DOCUMENT_TYPE_CHOICES = [
    ('dni', 'DNI'),
    ('ruc', 'RUC'),
    ('ce', 'CE'),
  ]
  document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES)
  document_number = models.CharField(max_length=12)
  email = models.CharField(max_length=50, null=True, blank=True)
  phone = models.CharField(max_length=9, null=True, blank=True)
  address = models.CharField(max_length=200, null=True, blank=True)
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
    db_table = 'customers'
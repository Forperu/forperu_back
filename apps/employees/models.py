from django.db import models

from apps.job_positions.models import JobPosition
from apps.warehouses.models import Warehouse

# Create your models here.
class Employee(models.Model):
  names = models.CharField(max_length=150)
  surname = models.CharField(max_length=50, null=True, blank=True)
  second_surname = models.CharField(max_length=50, null=True, blank=True)
  photo = models.CharField(max_length=150, null=True, blank=True)
  warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, db_column='warehouse_id')
  DOCUMENT_TYPE_CHOICES = [
    ('dni', 'DNI'),
    ('ce', 'CE'),
  ]
  document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES)
  document_number = models.CharField(max_length=9)
  birth_date = models.DateField()
  GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
  ]
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  email = models.CharField(max_length=100, null=True, blank=True)
  phone = models.CharField(max_length=9, null=True, blank=True)
  address = models.CharField(max_length=200, null=True, blank=True)
  hire_date = models.DateField()
  job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, db_column='job_position_id', null=True, blank=True)
  salary = models.DecimalField(max_digits=14, decimal_places=2)
  status = models.BooleanField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'employees'
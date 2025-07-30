from rest_framework import serializers
from apps.employees.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Employee
    fields = ['id', 'document_number', 'names', 'surname', 'second_surname', 'status', 'warehouse_id']
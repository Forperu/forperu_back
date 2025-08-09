from rest_framework import serializers
from .models import EmployeeBenefit
from apps.employees.serializers import EmployeeSerializer

class EmployeeBenefitSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    employee_id = serializers.IntegerField()
    status = serializers.BooleanField()
    
    class Meta:
        model = EmployeeBenefit
        fields = [
            'id',
            'employee_id',
            'employee',
            'benefit_type',
            'description',
            'amount',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
    
    def get_employee(self, obj):
        if obj.employee:
            EmployeeSerializer.Meta.model = obj.employee.__class__
            return EmployeeSerializer(obj.employee).data
        return None
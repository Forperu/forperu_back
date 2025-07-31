from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from apps.companies.serializers import CompanySerializer
from apps.employees.serializers import EmployeeSerializer
from apps.roles.serializers import RoleSerializer

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
  company_id = serializers.IntegerField(required=False, allow_null=True)
  employee_id = serializers.IntegerField(required=False, allow_null=True)
  role_id = serializers.IntegerField(required=False, allow_null=True)
  
  class Meta(UserCreateSerializer.Meta):
    model = User
    fields = [
      'id', 'company_id', 'username', 'employee_id', 'avatar', 
      'email', 'password', 'settings', 'shortcuts', 'status', 'role_id'
    ]

# Serializador principal de usuario
class UserSerializer(serializers.ModelSerializer):
  company = serializers.SerializerMethodField()
  employee = serializers.SerializerMethodField()
  role = serializers.SerializerMethodField()
  status = serializers.IntegerField()
  
  class Meta:
    model = User
    fields = [
      'id', 'username', 'avatar', 'email', 'status',
      'company', 'company_id', 'employee', 'employee_id',
      'role', 'role_id', 'settings', 'shortcuts'
    ]
    extra_kwargs = {
      'company_id': {'required': False, 'allow_null': True},
      'employee_id': {'required': False, 'allow_null': True},
      'role_id': {'required': False, 'allow_null': True}
    }
  
  def get_company(self, obj):
    if obj.company:
      CompanySerializer.Meta.model = obj.company.__class__
      return CompanySerializer(obj.company).data
    return None
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
  
  def get_role(self, obj):
    if obj.role:
      RoleSerializer.Meta.model = obj.role.__class__
      return RoleSerializer(obj.role).data
    return None

class UserPublicSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'avatar', 'email']
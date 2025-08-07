from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from apps.companies.serializers import CompanySerializer
from apps.employees.serializers import EmployeeSerializer
from apps.roles.serializers import RoleSerializer

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
  company_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
  employee_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
  role_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
  
  class Meta(UserCreateSerializer.Meta):
    model = User
    fields = [
      'id', 'company_id', 'username', 'employee_id', 'avatar', 
      'email', 'password', 'settings', 'shortcuts', 'status', 'role_id',
      'is_staff', 'is_superuser'
    ]
    extra_kwargs = {
      'password': {'write_only': True}
    }

  def create(self, validated_data):
    # Extraemos los IDs de las relaciones
    company_id = validated_data.pop('company_id', None)
    employee_id = validated_data.pop('employee_id', None)
    role_id = validated_data.pop('role_id', None)
    
    # Creamos el usuario
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)  # Esto encripta la contraseña correctamente
    
    # Asignamos las relaciones si existen
    if company_id:
      user.company_id = company_id
    if employee_id:
      user.employee_id = employee_id
    if role_id:
      user.role_id = role_id
        
    user.save()
    return user

class UserUpdateSerializer(serializers.ModelSerializer):
  company_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
  employee_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
  role_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
  password = serializers.CharField(required=False, write_only=True, allow_blank=True)

  class Meta:
    model = User
    fields = [
      'id', 'username', 'email', 'password', 'avatar',
      'company_id', 'employee_id', 'role_id', 'status',
      'settings', 'shortcuts', 'is_staff', 'is_superuser'
    ]
    extra_kwargs = {
      'email': {'required': False},
      'username': {'required': False}
    }

  def update(self, instance, validated_data):
    # Manejo de la contraseña si se proporciona
    password = validated_data.pop('password', None)
    if password:
      instance.set_password(password)

    # Actualización de relaciones
    for field in ['company_id', 'employee_id', 'role_id']:
      if field in validated_data:
        setattr(instance, field, validated_data.pop(field))

    # Actualización de los demás campos
    for attr, value in validated_data.items():
      setattr(instance, attr, value)

    instance.save()
    return instance
    
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
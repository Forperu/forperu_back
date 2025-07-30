import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
  AbstractBaseUser,
  PermissionsMixin,
  BaseUserManager
)

from apps.companies.models import Company
from apps.employees.models import Employee
from apps.roles.models import Role

class UserAccountManager(BaseUserManager):
  RESTRICTED_USERNAMES = ["admin", "undefined", "null", "superuser", "root", "system"]
  
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError("Users must have an email address.")
    
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)

    username = extra_fields.get("username", None)
    if username and username.lower() in self.RESTRICTED_USERNAMES:
      raise ValueError(f"The username '{username}' is not allowed.")
    
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, password, **extra_fields):
    user = self.create_user(email, password, **extra_fields)
    user.is_superuser = True
    user.is_staff = True
    user.status = True
    user.save(using=self._db)
    return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
  id = models.AutoField(primary_key=True)
  company = models.ForeignKey(Company, on_delete=models.SET_NULL, db_column='company_id', null=True, blank=True, related_name='users')
  role = models.ForeignKey(Role, on_delete=models.SET_NULL, db_column='role_id', null=True, blank=True, related_name='users')
  username = models.CharField(max_length=100, unique=True)
  employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, db_column='employee_id', null=True, blank=True, related_name='users')
  avatar = models.CharField(max_length=150, null=True, blank=True)
  email = models.EmailField(unique=True)
  settings = models.JSONField(default=dict, blank=True, null=True)
  shortcuts = models.JSONField(default=list, blank=True, null=True)
  status = models.BooleanField(default=True)
  
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  objects = UserAccountManager()
  
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username"]

  class Meta:
    db_table = 'users'

  def __str__(self):
    return self.email

  def save(self, *args, **kwargs):
    self.updated_at = timezone.now()
    super().save(*args, **kwargs)
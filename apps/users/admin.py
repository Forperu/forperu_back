from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class UserAccountAdmin(UserAdmin):
  list_display = (
    'id', 'email', 'username', 'company_id', 'role_id',
    'status', 'is_staff', 'created_at'
  )
  list_filter = ('status', 'is_staff', 'is_superuser', 'created_at')
  search_fields = ('email', 'username', 'company_id')
  ordering = ('email',)
  
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal Info', {
      'fields': (
        'username', 'company_id', 'role_id', 'employee_id',
        'avatar', 'settings', 'shortcuts'
      )
    }),
    ('Permissions', {
      'fields': ('status', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    }),
    ('Important dates', {'fields': ('created_at', 'updated_at', 'deleted_at')}),
  )
  
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': (
        'email', 'username', 'password1', 'password2',
        'company_id', 'role_id', 'status', 'is_staff'
      ),
    }),
  )
  
  readonly_fields = ('created_at', 'updated_at', 'deleted_at')

admin.site.register(UserAccount, UserAccountAdmin)
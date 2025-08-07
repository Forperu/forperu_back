from django.contrib import admin
from .models import WorkSchedule

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
  list_display = ('name', 'is_default', 'status', 'created_at')
  list_filter = ('is_default', 'status')
  search_fields = ('name', 'description')
  ordering = ('name',)
  fieldsets = (
    (None, {
      'fields': ('name', 'description')
    }),
    ('Configuración', {
      'fields': ('is_default', 'status')
    }),
    ('Fechas', {
      'fields': ('created_at', 'updated_at', 'deleted_at'),
      'classes': ('collapse',)
    })
  )
  readonly_fields = ('created_at', 'updated_at', 'deleted_at')
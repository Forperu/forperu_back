from django.db import models
from apps.systems.models import System  # Asumiendo que System está en apps.systems
from django.core.exceptions import ValidationError

class Key(models.Model):
  system = models.ForeignKey(
    System,
    on_delete=models.SET_NULL,
    db_column='system_id',
    null=True,
    blank=True,
    related_name='keys',
    verbose_name='Sistema asociado',
    help_text='Sistema al que pertenece esta clave (Odoo, Nubefact, SUNAT, etc.)'
  )
  name = models.CharField(
    max_length=100,
    verbose_name='Nombre de la clave',
    help_text='Nombre descriptivo de la configuración'
  )
  description = models.TextField(
    verbose_name='Descripción',
    help_text='Explicación detallada del propósito de esta clave',
    null=True,
    blank=True
  )
  config_key = models.CharField(
    max_length=100,
    verbose_name='Clave de configuración',
    help_text='Identificador único para esta configuración'
  )
  config_value = models.TextField(
    verbose_name='Valor de configuración',
    help_text='Valor asociado a esta clave de configuración'
  )
  created_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='created_by',
    related_name='created_keys',
    verbose_name='Creado por'
  )
  updated_by = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    db_column='updated_by',
    related_name='updated_keys',
    verbose_name='Actualizado por'
  )
  status = models.BooleanField(
    default=True,
    verbose_name='Estado',
    help_text='Indica si la clave está activa (1) o inactiva (0)'
  )
  created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Fecha de creación'
  )
  updated_at = models.DateTimeField(
    auto_now=True,
    null=True,
    blank=True,
    verbose_name='Fecha de actualización'
  )

  class Meta:
    db_table = 'keys'  # Nombre de la tabla en la base de datos
    verbose_name = 'Clave de configuración'
    verbose_name_plural = 'Claves de configuración'

  def __str__(self):
    return f"{self.system.name if self.system else 'Sistema'} - {self.config_key}"
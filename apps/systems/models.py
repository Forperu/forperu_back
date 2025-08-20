from django.db import models

class System(models.Model):
  name = models.CharField(
    max_length=100,
    verbose_name='Nombre del sistema',
    help_text='Nombre identificatorio del sistema'
  )
  description = models.TextField(
    verbose_name='Descripción',
    help_text='Descripción detallada del sistema',
    null=True,
    blank=True
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
    db_table = 'systems'
    verbose_name = 'Sistema'
    verbose_name_plural = 'Sistemas'
    ordering = ['name']

  def __str__(self):
    return self.name
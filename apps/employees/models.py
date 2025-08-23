import os
import uuid
from datetime import datetime
from django.utils import timezone
from django.core.files.storage import default_storage
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from apps.job_positions.models import JobPosition
from apps.warehouses.models import Warehouse

def employee_image_upload_path(instance, filename):
  # extensión original (jpg, png, etc.)
  ext = filename.split('.')[-1]
  # nomenclatura: employee_<id>_<timestamp>.<ext>
  filename = f"employee_{instance.id or uuid.uuid4()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
  return os.path.join("images/employees/", filename)

def employee_document_upload_path(instance, filename):
  ext = filename.split('.')[-1]
  filename = f"document_{instance.id or uuid.uuid4()}_{uuid.uuid4()}.{ext}"
  return os.path.join("documents/employees/", filename)

# Create your models here.
class Employee(models.Model):
  names = models.CharField(max_length=150)
  surname = models.CharField(max_length=50, null=True, blank=True)
  second_surname = models.CharField(max_length=50, null=True, blank=True)
  photo = models.ImageField(upload_to=employee_image_upload_path, null=True, blank=True)
  warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, db_column='warehouse_id', null=True, blank=True)
  DOCUMENT_TYPE_CHOICES = [
    ('dni', 'DNI'),
    ('ce', 'CE'),
  ]
  document_type = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES)
  document_number = models.CharField(max_length=9)
  birth_date = models.DateField(null=True, blank=True)
  GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
  ]
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  email = models.CharField(max_length=100, null=True, blank=True)
  phone = models.CharField(max_length=9, null=True, blank=True)
  address = models.CharField(max_length=200, null=True, blank=True)
  hire_date = models.DateField(null=True, blank=True)
  job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, db_column='job_position_id', null=True, blank=True)
  documents = models.JSONField(
    default=list,
    encoder=DjangoJSONEncoder,
    help_text="Lista de documentos en formato JSON"
  )
  salary = models.DecimalField(max_digits=14, decimal_places=2)
  status = models.BooleanField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    managed = True
    db_table = 'employees'
  
  def add_uploaded_file(self, uploaded_file):
    # Ruta final en storage
    storage_path = employee_document_upload_path(self, uploaded_file.name)
    saved_path = default_storage.save(storage_path, uploaded_file)
    file_url = default_storage.url(saved_path)

    doc = {
      'id': str(uuid.uuid4()),
      'name': os.path.basename(uploaded_file.name),
      'file': saved_path,           # ruta relativa en storage (para poder borrarlo luego)
      'url': file_url,              # URL accesible (MEDIA_URL + path)
      'type': uploaded_file.content_type or 'application/pdf',
      'size': uploaded_file.size,
      'uploaded_at': datetime.now().isoformat()
    }

    current_documents = list(self.documents or [])
    current_documents.append(doc)
    self.documents = current_documents
    self.save()  # ¡Importante: guardar los cambios!
    return doc

  def remove_document(self, document_id, delete_file=True):
    if not self.documents:
      return False

    remaining = []
    removed = False
    for doc in self.documents:
      if doc.get('id') == document_id:
        removed = True
        # Borra también el archivo del storage si corresponde
        if delete_file and doc.get('file'):
          try:
            default_storage.delete(doc['file'])
          except Exception:
            pass
      else:
        remaining.append(doc)

    self.documents = remaining
    return removed

  def get_documents(self):
      return self.documents or []

  def get_document_by_id(self, document_id):
    for doc in self.documents or []:
      if doc.get('id') == document_id:
        return doc
    return None

  def touch(self):
    self.updated_at = timezone.now()
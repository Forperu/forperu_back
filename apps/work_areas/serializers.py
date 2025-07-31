from rest_framework import serializers
from apps.work_areas.models import WorkArea

class WorkAreaSerializer(serializers.ModelSerializer):
  class Meta:
    model = WorkArea
    fields = ['id', 'name', 'description', 'status', 'created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at']
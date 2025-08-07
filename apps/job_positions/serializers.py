from rest_framework import serializers
from apps.job_positions.models import JobPosition
from apps.work_areas.serializers import WorkAreaSerializer

class JobPositionSerializer(serializers.ModelSerializer):
  work_area = serializers.SerializerMethodField()
  work_area_id = serializers.IntegerField()
  status = serializers.IntegerField()

  class Meta:
    model = JobPosition
    fields = [
      'id',
      'work_area_id',
      'work_area',
      'name',
      'description',
      'status',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]

  def get_work_area(self, obj):
    if obj.work_area:
      WorkAreaSerializer.Meta.model = obj.work_area.__class__
      return WorkAreaSerializer(obj.work_area).data
    return None
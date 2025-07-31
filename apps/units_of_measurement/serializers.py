from rest_framework import serializers
from apps.units_of_measurement.models import UnitOfMeasurement

class UnitOfMeasurementSerializer(serializers.ModelSerializer):
  class Meta:
    model = UnitOfMeasurement
    fields = ['id', 'name', 'shortcut', 'description', 'status', 'created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at']
from rest_framework import serializers
from .models import PerformanceReview
from apps.employees.serializers import EmployeeSerializer

class PerformanceReviewSerializer(serializers.ModelSerializer):
  employee = serializers.SerializerMethodField()
  reviewer = serializers.SerializerMethodField()
  employee_id = serializers.IntegerField()
  reviewer_id = serializers.IntegerField()
  
  class Meta:
    model = PerformanceReview
    fields = [
      'id',
      'employee_id',
      'employee',
      'reviewer_id',
      'reviewer',
      'review_date',
      'next_review_date',
      'performance_score',
      'strengths',
      'areas_for_improvement',
      'comments',
      'status',
      'acknowledged_at',
      'created_at',
      'updated_at',
      'deleted_at'
    ]
  
  def get_employee(self, obj):
    if obj.employee:
      EmployeeSerializer.Meta.model = obj.employee.__class__
      return EmployeeSerializer(obj.employee).data
    return None
  
  def get_reviewer(self, obj):
    if obj.reviewer:
      EmployeeSerializer.Meta.model = obj.reviewer.__class__
      return EmployeeSerializer(obj.reviewer).data
    return None
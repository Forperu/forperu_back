from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from eth_typing import ValidationError
from apps.employees.models import Employee

# Create your models here.
class PerformanceReview(models.Model):
  DRAFT = 'draft'
  COMPLETED = 'completed'
  ACKNOWLEDGED = 'acknowledged'
  
  STATUS_CHOICES = [
    (DRAFT, 'Draft'),
    (COMPLETED, 'Completed'),
    (ACKNOWLEDGED, 'Acknowledged'),
  ]
  
  employee = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    db_column='employee_id',
    related_name='performance_reviews'
  )
  reviewer = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    db_column='reviewer_id',
    related_name='conducted_reviews'
  )
  review_date = models.DateField()
  next_review_date = models.DateField(null=True, blank=True)
  performance_score = models.SmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)],
    null=True,
    blank=True
  )
  strengths = models.TextField(null=True, blank=True)
  areas_for_improvement = models.TextField(null=True, blank=True)
  comments = models.TextField(null=True, blank=True)
  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default=DRAFT
  )
  acknowledged_at = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True, blank=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'performance_reviews'
    verbose_name = 'Performance Review'
    verbose_name_plural = 'Performance Reviews'

  def clean(self):
    if self.next_review_date and self.next_review_date <= self.review_date:
      raise ValidationError("Next review date must be after the current review date")

  def __str__(self):
    return f"Review for {self.employee} on {self.review_date} (Score: {self.performance_score})"
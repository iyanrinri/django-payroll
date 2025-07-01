from django.db import models
from .user_model import User

class Salary(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Salaries'
        indexes = [
            models.Index(fields=['user_id'], name='idx_salary_user_id'),
        ]
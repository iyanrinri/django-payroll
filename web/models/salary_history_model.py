from django.db import models
from .user_model import User

class SalaryHistory(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'SalaryHistories'
        indexes = [
            models.Index(fields=['user_id'], name='idx_salary_history_user_id'),
        ]
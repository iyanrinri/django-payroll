from django.db import models

from .payroll_period_model import PayrollPeriod
from .user_model import User


class Overtime(models.Model):
    clock_date = models.DateField()
    hours = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    class Meta:
        ordering = ['clock_date']
        verbose_name_plural = 'Overtimes'
        indexes = [
            models.Index(fields=['user_id'], name='idx_overtime_user_id'),
            models.Index(fields=['payroll_period_id'], name='idx_overtime_pp_id'),
            models.Index(fields=['clock_date'], name='idx_overtime_clock_date'),
        ]
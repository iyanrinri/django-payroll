from django.db import models

from .payroll_period_model import PayrollPeriod
from .user_model import User

class Attendance(models.Model):
    clock_date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    class Meta:
        ordering = ['clock_date']
        unique_together = ('user', 'clock_date')
        verbose_name_plural = 'Attendances'
        indexes = [
            models.Index(fields=['user_id'], name='idx_attendance_user_id'),
            models.Index(fields=['payroll_period_id'], name='idx_attendance_pp_id'),
            models.Index(fields=['clock_date'], name='idx_attendance_clock_date'),
            models.Index(fields=['clock_in'], name='idx_attendance_payroll_ci'),
            models.Index(fields=['clock_out'], name='idx_attendance_payroll_co'),
        ]
from django.db import models

class Payroll(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    payroll_period = models.ForeignKey('PayrollPeriod', on_delete=models.CASCADE)
    basic_salary = models.FloatField()
    salary_per_hour = models.FloatField()
    attended_days = models.IntegerField()
    attended_percentage = models.FloatField()
    overtime_hours = models.FloatField()
    overtime_pay = models.FloatField()
    reimbursement_amount = models.FloatField()
    take_home_salary = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Payrolls'
        indexes = [
            models.Index(fields=['created_at'], name='idx_payroll_created_at'),
        ]

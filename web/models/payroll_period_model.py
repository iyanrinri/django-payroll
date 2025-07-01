from django.db import models

class PayrollPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.start_date.strftime('%B %Y') + ' - ' + self.end_date.strftime('%B %Y')
    class Meta:
        ordering = ['start_date']
        verbose_name_plural = 'PayrollPeriods'
        indexes = [
            models.Index(fields=['start_date'], name='idx_payroll_period_start_date'),
            models.Index(fields=['end_date'], name='idx_payroll_period_end_date'),
        ]

from django.db import models
from .user_model import User
from .payroll_period_model import PayrollPeriod

class Reimbursement(models.Model):
    claim_date = models.DateField()
    amount = models.FloatField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    class Meta:
        ordering = ['claim_date']
        verbose_name_plural = 'Reimbursements'
        indexes = [
            models.Index(fields=['user_id'], name='idx_reimbursement_user_id'),
            models.Index(fields=['claim_date'], name='idx_reimbursement_claim_date'),
            models.Index(fields=['payroll_period_id'], name='idx_reimbursement_pp_id'),
        ]

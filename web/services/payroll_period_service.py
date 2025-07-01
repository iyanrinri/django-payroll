from django.utils import timezone
from rest_framework.exceptions import ValidationError

from web.models import PayrollPeriod


def get_payroll_period():
    today = timezone.now().date()
    payroll_period = PayrollPeriod.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).first()

    if not payroll_period:
        raise ValidationError({"error": "There is no payroll period for today, admin has not created one yet."})

    return payroll_period
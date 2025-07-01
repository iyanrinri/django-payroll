from django.utils import timezone
from rest_framework.exceptions import ValidationError

from web.models import Overtime
from web.services.payroll_period_service import get_payroll_period

def validate_hours(hours):
    if hours is None:
        raise ValidationError({"hours": "Field Hours is required"})
    if hours <= 0:
        raise ValidationError({"hours": "Field Hours must be greater than 0"})
    if hours > 3:
        raise ValidationError({"hours": "Field Hours maximal is 3 hours"})

def create_overtime_by_request(request, validated_data: dict):
    today = timezone.now().date()

    payroll_period = get_payroll_period()

    user = request.user
    overtime, created = Overtime.objects.get_or_create(
        user=user,
        clock_date=today,
        payroll_period=payroll_period,
        defaults={
            'hours': validated_data['hours']
        }
    )
    if not created:
        overtime.hours = validated_data['hours']
        overtime.save()
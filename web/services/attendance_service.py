from django.utils import timezone
from rest_framework.exceptions import ValidationError

from web.models import Attendance, PayrollPeriod

def handle_attendance(user):
    today = timezone.now().date()

    payroll_period = PayrollPeriod.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).first()

    if not payroll_period:
        raise ValidationError({"error":"Tidak ada payroll period yang aktif admin belum menambahkan."})

    attendance, created = Attendance.objects.get_or_create(clock_date=today, user=user, defaults={'clock_date': today, 'clock_in': timezone.now(), 'payroll_period': payroll_period})

    # always update clock-out if not created (exists)
    if not created:
        attendance.clock_out = timezone.now()
        attendance.save()

    return attendance
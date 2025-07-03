from django.utils import timezone
from rest_framework.exceptions import ValidationError

from web.models.attendance_model import Attendance
from web.models.payroll_period_model import PayrollPeriod
from datetime import datetime

from web.services.payroll_period_service import get_payroll_period

def get_current_attendance(user):
    today = timezone.now().date()
    payroll_period = PayrollPeriod.objects.filter(start_date__lte=today, end_date__gte=today).first()
    return Attendance.objects.filter(user=user, payroll_period=payroll_period, clock_date=today).first()

def get_attendance(user):
    today = timezone.now().date()
    payroll_period = PayrollPeriod.objects.filter(start_date__lte=today, end_date__gte=today).first()
    return Attendance.objects.filter(user=user, payroll_period=payroll_period).order_by('-clock_date').all()

def handle_attendance(user):
    today = timezone.now().date()

    payroll_period = get_payroll_period()

    if not today.weekday():
        raise ValidationError({"error":"Attendance Clock cannot do in weekends."})

    attendance, created = Attendance.objects.get_or_create(clock_date=today, user=user, defaults={'clock_date': today, 'clock_in': timezone.now().time(), 'payroll_period': payroll_period})
    if not created:
        attendance.clock_out = timezone.now().time()
        clock_in_dt = datetime.combine(today, attendance.clock_in)
        clock_out_dt = datetime.combine(today, attendance.clock_out)
        attendance.duration = clock_out_dt - clock_in_dt
        attendance.save()

    return attendance
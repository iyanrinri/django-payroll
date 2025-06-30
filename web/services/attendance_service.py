from django.utils import timezone
from web.models import Attendance
# from rest_framework.exceptions import ValidationError

def handle_attendance(user):
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(clock_date=today, user=user, defaults={'clock_date': today, 'clock_in': timezone.now()})

    # always update clock-out if not created (exists)
    if not created:
        attendance.clock_out = timezone.now()
        attendance.save()

    return attendance
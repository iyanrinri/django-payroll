from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from tqdm import tqdm
from django.db import transaction

from web.models import PayrollPeriod, Attendance, Overtime, Reimbursement
from django.utils import timezone
from datetime import timedelta, date
import random
from datetime import datetime

User = get_user_model()

class Command(BaseCommand):
    help = "Seed 10,000 dummy attendances, overtimes, reimbursements"

    def handle(self, *args, **kwargs):
        fake = Faker()
        self.stdout.write(self.style.WARNING("Seeding attendances, overtimes, and reimbursement..."))
        payroll_period, created = PayrollPeriod.objects.get_or_create(start_date='2025-07-01', end_date='2025-07-31')
        users = User.objects.filter(role='EMPLOYEE', is_active=True)
        for user in tqdm(users, desc="Seeding users actions.."):
            with transaction.atomic():
                for _ in range(22):
                    attendance = fake.date_between(
                        start_date=date(2025, 7, 1),
                        end_date=date(2025, 7, 31)
                    )
                    clock_in = timezone.now()
                    hours_added = random.randint(2, 6)
                    clock_out = clock_in + timedelta(hours=hours_added)
                    overtime = fake.random_int(min=0, max=3)
                    reimbursement = fake.random_int(min=0, max=100000)
                    try:
                        day = timezone.now().date()
                        clock_in_dt = datetime.combine(day, clock_in.time())
                        clock_out_dt = datetime.combine(day, clock_out.time())
                        duration = clock_out_dt - clock_in_dt
                        Attendance.objects.get_or_create(clock_date=attendance, user=user, payroll_period=payroll_period, clock_in=clock_in.time(), clock_out=clock_out.time(), duration=duration)
                    except Exception as e:
                        # self.stdout.write(self.style.SUCCESS(f"duplicate attendance: {e}"))
                        pass

                    if overtime > 0:
                        Overtime.objects.get_or_create(clock_date=attendance, user=user, payroll_period=payroll_period, hours=overtime)
                    if reimbursement > 0 & fake.random_int(min=0, max=1005) % 6 == 0:
                        Reimbursement.objects.get_or_create(claim_date=attendance, user=user, payroll_period=payroll_period, amount=reimbursement)

        self.stdout.write(self.style.SUCCESS(f"created successfully."))

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from tqdm import tqdm
from django.db import transaction

from web.models import Salary, SalaryHistory  # sesuaikan dengan lokasi modelmu

User = get_user_model()

class Command(BaseCommand):
    help = "Seed 10,000 dummy users with salary & salary history"

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = 10_000
        batch_size = 500  # lebih kecil karena kita tidak pakai bulk_create

        self.stdout.write(self.style.WARNING("Seeding users, salaries, and salary histories..."))

        for _ in tqdm(range(total)):
            with transaction.atomic():
                email = fake.unique.email()
                name = fake.name()
                password = email  # default password = email
                salary_amount = fake.random_int(min=3_000_000, max=15_000_000)

                # Create user
                user = User(
                    name=name,
                    email=email,
                    role="EMPLOYEE",
                )
                user.set_password(password)
                user.save()

                salary, created = Salary.objects.get_or_create(user=user, defaults={
                    'amount': salary_amount
                })

                if not created:
                    salary.amount = salary_amount
                    salary.save()

                # Create salary history
                SalaryHistory.objects.create(
                    user=user,
                    amount=salary.amount
                )

        self.stdout.write(self.style.SUCCESS(f"{total} users, salaries, and salary histories created successfully."))

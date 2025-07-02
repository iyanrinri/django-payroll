from celery import shared_task

from web.models import PayrollPeriod
from web.services.payroll_service import run_payroll
from web.models.user_model import User


@shared_task
def add(x, y):
    result = x + y
    print("task result: " + str(result))
    return result

@shared_task
def run_payroll_task(payroll_period_id):
    payroll_period = PayrollPeriod.objects.get(id=payroll_period_id)
    users = User.objects.filter(role='EMPLOYEE', is_active=True)
    run_payroll(users, payroll_period)
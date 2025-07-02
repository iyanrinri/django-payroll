from ..models.salary_model import Salary
from ..models.attendance_model import Attendance
from ..models.payroll_model import Payroll
from django.utils import timezone

def run_payroll(users, payroll_period):
    for user in users.all():
        salary = Salary.objects.filter(user=user).first()
        basic_salary = salary.amount
        attended_days = 0
        attendances = Attendance.objects.filter(user=user, payroll_period=payroll_period)
        for attendance in attendances:
            if attendance.clock_in and attendance.clock_out:
                attended_days += 1

        attended_percentage = attended_days * 100 / 22
        if attended_percentage > 100:
            attended_percentage = 100
        overtime_hours = 0
        overtimes = user.overtime_set.filter(payroll_period=payroll_period, user=user)
        for overtime in overtimes:
            overtime_hours += overtime.hours

        salary_per_hour = basic_salary / 22
        overtime_pay = overtime_hours * salary_per_hour * 1.5

        reimbursement_amount = 0
        reimbursements = user.reimbursement_set.filter(payroll_period=payroll_period, user=user)
        for reimbursement in reimbursements:
            reimbursement_amount += reimbursement.amount

        take_home_salary = (basic_salary * (attended_percentage / 100)) + overtime_pay + reimbursement_amount
        Payroll.objects.create(
            user=user,
            basic_salary=basic_salary,
            salary_per_hour=salary_per_hour,
            attended_days=attended_days,
            attended_percentage=attended_percentage,
            overtime_hours=overtime_hours,
            overtime_pay=overtime_pay,
            reimbursement_amount=reimbursement_amount,
            payroll_period=payroll_period,
            take_home_salary=take_home_salary
        )

        print(f"Payroll for {user.name} created successfully.")

    payroll_period.processed_at = timezone.now()
    payroll_period.save()
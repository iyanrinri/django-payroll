from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=100, default='EMPLOYEE')
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'], name='idx_user_email'),
            models.Index(fields=['role'], name='idx_user_role'),
        ]

class PayrollPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.start_date.strftime('%B %Y') + ' - ' + self.end_date.strftime('%B %Y')
    class Meta:
        ordering = ['start_date']
        verbose_name_plural = 'PayrollPeriods'
        indexes = [
            models.Index(fields=['start_date'], name='idx_payroll_period_start_date'),
            models.Index(fields=['end_date'], name='idx_payroll_period_end_date'),
        ]

class Attendance(models.Model):
    clock_date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    class Meta:
        ordering = ['clock_date']
        unique_together = ('user', 'clock_date')
        verbose_name_plural = 'Attendances'
        indexes = [
            models.Index(fields=['user_id'], name='idx_attendance_user_id'),
            models.Index(fields=['payroll_period_id'], name='idx_attendance_pp_id'),
            models.Index(fields=['clock_date'], name='idx_attendance_clock_date'),
            models.Index(fields=['clock_in'], name='idx_attendance_payroll_ci'),
            models.Index(fields=['clock_out'], name='idx_attendance_payroll_co'),
        ]

class Overtime(models.Model):
    clock_date = models.DateField()
    hours = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    class Meta:
        ordering = ['clock_date']
        verbose_name_plural = 'Overtimes'
        indexes = [
            models.Index(fields=['user_id'], name='idx_overtime_user_id'),
            models.Index(fields=['payroll_period_id'], name='idx_overtime_pp_id'),
            models.Index(fields=['clock_date'], name='idx_overtime_clock_date'),
        ]

class Reimbursement(models.Model):
    claim_date = models.DateField()
    amount = models.FloatField()
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

class Salary(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Salaries'
        indexes = [
            models.Index(fields=['user_id'], name='idx_salary_user_id'),
        ]

class SalaryHistory(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'SalaryHistories'
        indexes = [
            models.Index(fields=['user_id'], name='idx_salary_history_user_id'),
        ]
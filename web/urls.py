from django.urls import path

from .views.claim_view import ReimbursementListCreateView, ReimbursementRetrieveUpdateDestroy
from .views.employee_view import EmployeeListCreateView, EmployeeRetrieveUpdateDestroy
from .views.overtime_view import OvertimeListCreateView, OvertimeRetrieveUpdateDestroy
from .views.payroll_period_view import PayrollPeriodListCreateView, PayrollPeriodRetrieveUpdateDestroy
from .views.attendance_view import AttendanceListView, AttendanceClock
from .views.auth_view import AuthLoginView, AuthLogoutView
from .views.salary_view import SalaryCreateForUserView, SalaryHistoryView
from .views.payroll_view import PayrollRunView, PayrollSummaryView
from .views.user_view import UserView

urlpatterns = [

    path('auth/login/', AuthLoginView.as_view(), name='auth-login'),
    path('auth/logout/', AuthLogoutView.as_view(), name='auth-logout'),
    path('user/', UserView.as_view(), name='user-profile'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroy.as_view(), name='employee-rud'),
    path('employees/<int:user_id>/salaries/', SalaryCreateForUserView.as_view(), name='create-employee-salary'),
    path('employees/<int:user_id>/salaries/history/', SalaryHistoryView.as_view(), name='history-employee-salary'),
    path('payroll-periods/', PayrollPeriodListCreateView.as_view(), name='payroll-list-create'),
    path('payroll-periods/<int:pk>/', PayrollPeriodRetrieveUpdateDestroy.as_view(), name='payroll-rud'),

    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/clock', AttendanceClock.as_view(), name='attendance-clock'),

    path('overtimes/', OvertimeListCreateView.as_view(), name='overtime-list-create'),
    path('overtimes/<int:pk>/', OvertimeRetrieveUpdateDestroy.as_view(), name='overtime-rud'),

    path('reimbursements/', ReimbursementListCreateView.as_view(), name='reimbursement-list-create'),
    path('reimbursements/<int:pk>/', ReimbursementRetrieveUpdateDestroy.as_view(), name='reimbursement-rud'),

    path('payroll/run/', PayrollRunView.as_view(), name='payroll-run'),
    path('payroll/summary', PayrollSummaryView.as_view(), name='payroll-summary')
]

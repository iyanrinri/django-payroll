from django.urls import path
from .views.employee_view import EmployeeListCreateView, EmployeeRetrieveUpdateDestroy
from .views.overtime_view import OvertimeListCreateView, OvertimeRetrieveUpdateDestroy
from .views.payroll_period_view import PayrollPeriodListCreateView, PayrollPeriodRetrieveUpdateDestroy
from .views.attendance_view import AttendanceListView, AttendanceClock
from .views.auth_view import AuthLogin

urlpatterns = [

    path('auth/login/', AuthLogin.as_view(), name='auth-login'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroy.as_view(), name='employee-rud'),
    path('payroll-periods/', PayrollPeriodListCreateView.as_view(), name='payroll-list-create'),
    path('payroll-periods/<int:pk>/', PayrollPeriodRetrieveUpdateDestroy.as_view(), name='payroll-rud'),

    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/clock', AttendanceClock.as_view(), name='attendance-clock'),

    path('overtimes/', OvertimeListCreateView.as_view(), name='overtime-list-create'),
    path('overtimes/<int:pk>/', OvertimeRetrieveUpdateDestroy.as_view(), name='overtime-rud'),
]

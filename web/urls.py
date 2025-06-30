from django.urls import path
from .views.employee import EmployeeListCreateView, EmployeeRetrieveUpdateDestroy
from .views.payroll_period import PayrollPeriodListCreateView, PayrollPeriodRetrieveUpdateDestroy
from .views.attendance import AttendanceListView, AttendanceClock
from .views.auth import AuthLogin

urlpatterns = [

    path('auth/login/', AuthLogin.as_view(), name='auth-login'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroy.as_view(), name='employee-rud'),
    path('payroll-periods/', PayrollPeriodListCreateView.as_view(), name='payroll-list-create'),
    path('payroll-periods/<int:pk>/', PayrollPeriodRetrieveUpdateDestroy.as_view(), name='payroll-rud'),

    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/clock', AttendanceClock.as_view(), name='attendance-clock')
]

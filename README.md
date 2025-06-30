
# Qlay Payroll Web API

## Main Features
- JWT/Token (Bearer) authentication
- User/Employee management (CRUD)
- Endpoint protection with Token Auth
- Swagger UI (http://localhost:8000/swagger/) for API documentation and testing

## Installation
1. Clone the repo and enter the project folder
2. (Optional) Create and activate a virtualenv
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser --email admin@example.com --name Admin
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

## Authentication
Use the following header to access protected endpoints:
```
Authorization: Bearer <token>
```
Token is obtained from the `/auth/login/` endpoint.

## API Testing
- Open Swagger: http://localhost:8000/swagger/
- Click Authorize, enter: `Bearer <token>`
- Try the `/employees/` endpoint and others

## Key Structure
- `web/models.py` : All main models (User, PayrollPeriod, Attendance, Overtime, Reimbursement, Salary, SalaryHistory)
- `web/serializers/employee_serializer.py` : User/Employee serializer
- `web/serializers/attendance_serializer.py` : Attendance serializer
- `web/serializers/payroll_period_serializer.py` : Payroll period serializer
- `web/views/auth.py` : Login endpoint
- `web/views/employee.py` : Employee CRUD (admin/authorized only)
- `web/views/payroll_period.py` : Payroll period CRUD
- `web/views/attendance.py` : Attendance endpoints (list, clock-in/out)
- `web/services/attendance_service.py` : Attendance business logic

## Notes
- All user CRUD endpoints are protected by token except login.
- For development, use SQLite. For production, change the DB in `settings.py`.

---

If you encounter errors or need help, please contact the maintainer.

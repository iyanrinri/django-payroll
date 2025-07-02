from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.response import Response

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import PayrollPeriod
from ..models.payroll_model import Payroll
from ..models.user_model import User
from ..permissions.admin_permission import IsAdminOrSuperUser
from ..serializers.payroll_serializer import PayrollSerializer
from ..services.payroll_period_service import get_payroll_period
from django.db.models import Q
from drf_yasg import openapi

from ..services.payroll_service import run_payroll


class PayrollRunView(APIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    @swagger_auto_schema(
        operation_id="payroll_run",
        operation_description="Payroll run current payroll period.",
        request_body=no_body,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        payroll_period = get_payroll_period()
        if payroll_period.processed_at:
            return Response({'message': "Payroll period already processed"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(role='EMPLOYEE', is_active=True)
        users_with_zero_salary = users.filter(Q(salary__isnull=True) | Q(salary=0))
        if users_with_zero_salary.exists():
            data = []
            for user in users_with_zero_salary:
                salary = getattr(user, 'salary', None)
                data.append({
                    "id": user.id,
                    "email": user.email,
                    "salary": salary.amount if salary else None
                })

            return Response({
                "zero_salaries": data,
                "message": "There are users with zero salary"
            }, status=400)

        run_payroll(users, payroll_period)

        return Response({'message': "Payroll run successfully"}, status=status.HTTP_200_OK)

class PayrollSummaryView(APIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'payroll_period_id',
                openapi.IN_QUERY,
                description="ID dari payroll period",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={200: PayrollSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        payroll_period_id = self.kwargs.get('payroll_period_id')
        if not payroll_period_id:
            payroll_period = get_payroll_period()
        else:
            payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)

        payrolls = Payroll.objects.filter(payroll_period=payroll_period)
        serializer = self.serializer_class(payrolls, many=True)
        return Response(serializer.data)

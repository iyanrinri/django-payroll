from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import PayrollPeriod
from ..models.payroll_model import Payroll
from ..models.user_model import User
from ..permissions.admin_permission import IsAdminOrSuperUser
from ..serializers.payroll_serializer import PayrollSerializer
from ..services.payroll_period_service import get_payroll_period
from ..tasks import run_payroll_task


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
            return Response(
                {"message": "Payroll period already processed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optimized query: avoid N+1 with select_related
        users_with_zero_salary = User.objects.filter(
            role='EMPLOYEE',
            is_active=True
        ).filter(
            Q(salary__isnull=True) | Q(salary__amount=0)
        ).select_related('salary')

        if users_with_zero_salary.exists():
            # Fast loop using list comprehension
            data = [
                {
                    "id": user.id,
                    "email": user.email,
                    "salary": user.salary.amount if user.salary else None
                }
                for user in users_with_zero_salary
            ]

            return Response(
                {
                    "zero_salaries": data,
                    "message": "There are users with zero salary"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Trigger Celery task or normal function
        run_payroll_task.delay(payroll_period.id)

        return Response(
            {"message": "Payroll please wait until processed at is done"},
            status=status.HTTP_200_OK
        )

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100

class PayrollSummaryView(generics.GenericAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    pagination_class = CustomPagination
    ordering_fields = ['id', 'take_home_salary', 'basic_salary']
    ordering = ['id', '-take_home_salary']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'payroll_period_id',
                openapi.IN_QUERY,
                description="ID dari payroll period",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="page number",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'per_page',
                openapi.IN_QUERY,
                description="Limit page size. Default is 10. Max is 100.",
                type=openapi.TYPE_NUMBER
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

        paginator = self.paginator
        queryset = self.get_queryset()
        queryset = queryset.filter(payroll_period=payroll_period)
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            return paginator.get_paginated_response(
                self.serializer_class(page, many=True).data
            )

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

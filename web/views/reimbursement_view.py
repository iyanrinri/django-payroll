
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.reimbursement_model import Reimbursement
from ..serializers.reimbursement_serializer import ReimbursementSerializer, ReimbursementCreateUpdateSerializer
from ..services.payroll_period_service import get_payroll_period


class CustomPaginationWithTotal(PageNumberPagination):
    page_size_query_param = 'per_page'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_amount = sum(item.amount for item in self.page.paginator.object_list)
        return Response({
            'count': self.page.paginator.count,
            'total_amount': total_amount,
            'total_amount_display': "{:,.2f}".format(total_amount),
            'page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'results': data
        })

class ReimbursementListCreateView(generics.ListCreateAPIView):
    queryset = Reimbursement.objects.all()
    serializer_class = ReimbursementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginationWithTotal

    def get_queryset(self):
        payroll_period = get_payroll_period()
        return Reimbursement.objects.filter(
            payroll_period=payroll_period,
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReimbursementCreateUpdateSerializer
        return ReimbursementSerializer

class ReimbursementRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reimbursement.objects.all()
    serializer_class =  ReimbursementSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReimbursementCreateUpdateSerializer
        return ReimbursementSerializer

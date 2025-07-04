
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models.overtime_model import Overtime
from ..serializers.overtime_serializer import OvertimeSerializer, OvertimeCreateUpdateSerializer
from ..services.payroll_period_service import get_payroll_period


class OvertimeListCreateView(generics.ListCreateAPIView):
    queryset = Overtime.objects.all()
    serializer_class = OvertimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        payroll_period = get_payroll_period()
        return Overtime.objects.filter(
            payroll_period=payroll_period,
            user=self.request.user
        )
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OvertimeCreateUpdateSerializer
        return OvertimeSerializer

class OvertimeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Overtime.objects.all()
    serializer_class =  OvertimeSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OvertimeCreateUpdateSerializer
        return OvertimeSerializer

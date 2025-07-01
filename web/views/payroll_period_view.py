
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models.payroll_period_model import PayrollPeriod
from ..permissions.admin_permission import IsAdminOrSuperUser
from ..serializers.payroll_period_serializer import PayrollPeriodSerializer

class PayrollPeriodListCreateView(generics.ListCreateAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

class PayrollPeriodRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class =  PayrollPeriodSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

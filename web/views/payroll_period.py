
from rest_framework import generics
from ..models import PayrollPeriod
from ..serializers.payroll_period_serializer import PayrollPeriodSerializer

class PayrollPeriodListCreateView(generics.ListCreateAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer

class PayrollPeriodRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class =  PayrollPeriodSerializer

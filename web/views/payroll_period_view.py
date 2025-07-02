from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models.payroll_period_model import PayrollPeriod
from ..permissions.admin_permission import IsAdminOrSuperUser
from ..serializers.payroll_period_serializer import PayrollPeriodSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from drf_yasg import openapi


class PayrollPeriodFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='start_date', lookup_expr='lte')
    end_date = filters.DateFilter(field_name='end_date', lookup_expr='gte')

    class Meta:
        model = PayrollPeriod
        fields = ['start_date', 'end_date']


class PayrollPeriodListCreateView(generics.ListCreateAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    filter_backends = [filters.DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = PayrollPeriodFilter
    ordering_fields = ['start_date', 'end_date']
    ordering = ['-start_date']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Filter tanggal mulai (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Filter tanggal akhir (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('ordering', openapi.IN_QUERY,
                              description="Urutan (contoh: ordering=start_date atau ordering=-start_date)",
                              type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PayrollPeriodRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

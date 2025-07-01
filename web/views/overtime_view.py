
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models.overtime_model import Overtime
from ..serializers.overtime_serializer import OvertimeSerializer, OvertimeCreateUpdateSerializer


class OvertimeListCreateView(generics.ListCreateAPIView):
    queryset = Overtime.objects.all()
    serializer_class = OvertimeSerializer
    permission_classes = [IsAuthenticated]

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


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models.reimbursement_model import Reimbursement
from ..serializers.reimbursement_serializer import ReimbursementSerializer, ReimbursementCreateUpdateSerializer


class ReimbursementListCreateView(generics.ListCreateAPIView):
    queryset = Reimbursement.objects.all()
    serializer_class = ReimbursementSerializer
    permission_classes = [IsAuthenticated]

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

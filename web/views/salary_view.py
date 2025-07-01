from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import SalaryHistory
from ..models.salary_model import Salary
from ..models.user_model import User
from ..permissions.admin_permission import IsAdminOrSuperUser
from ..serializers.salary_history_serializer import SalaryHistorySerializer
from ..serializers.salary_serializer import SalarySerializer
from rest_framework.exceptions import NotFound

class SalaryCreateForUserView(generics.CreateAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

        with transaction.atomic():
            salary, created = Salary.objects.get_or_create(user=user, defaults={
                'amount': serializer.validated_data['amount']
            })

            if not created:
                salary.amount = serializer.validated_data['amount']
                salary.save()

            SalaryHistory.objects.create(
                user=user,
                amount=salary.amount
            )

class SalaryHistoryView(generics.ListAPIView):
    serializer_class = SalaryHistorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")

        return SalaryHistory.objects.filter(user=user).order_by('-created_at')


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        all_histories = list(queryset)
        serializer = self.get_serializer(
            all_histories,
            many=True,
            context={'request': request, 'all_histories': all_histories}
        )
        return Response(serializer.data)
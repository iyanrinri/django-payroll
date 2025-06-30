
from rest_framework import generics, permissions
from ..models import User
from ..permissions.admin_permission import IsAdminOrSuperUser
from ..serializers.employee_serializer import UserSerializer

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]

class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class =  UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]

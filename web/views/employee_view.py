from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg import openapi

from ..models.user_model import User
from ..permissions.admin_permission import IsAdminOrSuperUser
from ..serializers.employee_serializer import UserSerializer

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'paginated',
                openapi.IN_QUERY,
                description="Set to `1` to enable pagination",
                type=openapi.TYPE_STRING
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
        ]
    )
    def get(self, request, *args, **kwargs):
        paginated = request.query_params.get('paginated') == '1'
        queryset = self.get_queryset()
        queryset = queryset.filter(role='EMPLOYEE')
        if paginated:
            paginator = self.paginator
            page = paginator.paginate_queryset(queryset, request, view=self)
            if page is not None:
                return paginator.get_paginated_response(
                    self.serializer_class(page, many=True).data
                )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]

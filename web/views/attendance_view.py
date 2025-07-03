from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi

from ..models.attendance_model import Attendance
from ..serializers.attendance_serializer import AttendanceSerializer
from ..services.attendance_service import handle_attendance, get_attendance, get_current_attendance


class AttendanceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get(self, request, *args, **kwargs):
        attendance = get_attendance(request.user)
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)


class AttendanceCurrentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer
    filter_backends = []
    pagination_class = None

    @swagger_auto_schema(
        operation_description="Get the current attendance for the authenticated user.",
        manual_parameters=[],
        responses={
            200: openapi.Response(
                description="OK",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "clock_date": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                                "clock_in": openapi.Schema(type=openapi.TYPE_STRING),
                                "clock_out": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                            }
                        )
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        attendance = get_current_attendance(request.user)
        if not attendance:
            return Response({'data': None})
        serializer = self.get_serializer(attendance)
        return Response({'data': serializer.data})


class AttendanceClock(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @swagger_auto_schema(
        operation_description="Clock-in or clock-out for the authenticated user. No body required.",
        request_body=None,
        responses={200: AttendanceSerializer}
    )
    def post(self, request, *args, **kwargs):
        attendance = handle_attendance(request.user)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.attendance_model import Attendance
from ..serializers.attendance_serializer import AttendanceSerializer
from ..services.attendance_service import handle_attendance, get_attendance

class AttendanceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get(self, request, *args, **kwargs):
        attendance = get_attendance(request.user)
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

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

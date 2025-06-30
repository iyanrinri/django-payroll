from rest_framework import serializers
from ..models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('id', 'clock_date', 'clock_in', 'clock_out', 'user', 'payroll_period', 'created_at', 'updated_at')

from rest_framework import serializers
from ..models.attendance_model import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    duration_display = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('id', 'clock_date', 'clock_in', 'clock_out', 'user', 'payroll_period', 'created_at', 'updated_at')

    def get_duration_display(self, obj):
        if obj.duration:
            total_seconds = int(obj.duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return None

from rest_framework import serializers
from ..models.attendance_model import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    clock_in_display = serializers.SerializerMethodField()
    clock_out_display = serializers.SerializerMethodField()
    clock_date_display = serializers.SerializerMethodField()
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

    def get_clock_date_display(self, obj):
        if obj.clock_date:
            return obj.clock_date.strftime('%a, %d %B %Y')
        return None

    def get_clock_in_display(self, obj):
        if obj.clock_in:
            return obj.clock_in.strftime('%H:%M:%S')
        return None

    def get_clock_out_display(self, obj):
        if obj.clock_out:
            return obj.clock_out.strftime('%H:%M:%S')
        return None

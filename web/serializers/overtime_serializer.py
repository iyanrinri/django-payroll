from rest_framework import serializers

from ..models.overtime_model import Overtime
from ..services.overtime_service import create_overtime_by_request, validate_hours


class OvertimeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = ['hours']

    def create(self, validated_data):
        request = self.context.get('request')
        overtime = create_overtime_by_request(request, validated_data)
        return overtime

    def update(self, instance, validated_data):
        instance.hours = validated_data.get('hours', instance.hours)
        instance.save()
        return instance

    def validate(self, data):
        validate_hours(data.get('hours'))
        return data

class OvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        overtime = create_overtime_by_request(request, validated_data)
        return overtime

    def update(self, instance, validated_data):
        instance.hours = validated_data.get('hours', instance.hours)
        instance.save()
        return instance

    def validate(self, data):
        validate_hours(data.get('hours'))
        return data

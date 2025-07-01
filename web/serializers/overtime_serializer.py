from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import PayrollPeriod
from ..models.overtime_model import Overtime
from django.utils import timezone

class OvertimeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = ['hours']

    def create(self, validated_data):
        today = timezone.now().date()

        payroll_period = PayrollPeriod.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        ).first()

        if not payroll_period:
            raise ValidationError({"error": "There is no payroll period for today, admin has not created one yet."})
        request = self.context.get('request')
        user = request.user
        overtime, created = Overtime.objects.get_or_create(
            user=user,
            clock_date=today,
            payroll_period=payroll_period,
            defaults={
                'hours': validated_data['hours']
            }
        )
        if not created:
            overtime.hours = validated_data['hours']
            overtime.save()
        return overtime

    def update(self, instance, validated_data):
        instance.hours = validated_data.get('hours', instance.hours)
        instance.save()
        return instance

    def validate(self, data):
        hours = data.get('hours')
        if hours is None:
            raise serializers.ValidationError({"hours": "Field Hours is required"})
        if hours <= 0:
            raise serializers.ValidationError({"hours": "Field Hours must be greater than 0"})
        if hours > 3:
            raise serializers.ValidationError({"hours": "Field Hours maximal is 3 hours"})
        return data

class OvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = '__all__'

    def create(self, validated_data):
        today = timezone.now().date()

        payroll_period = PayrollPeriod.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        ).first()

        if not payroll_period:
            raise ValidationError({"error": "There is no payroll period for today, admin has not created one yet."})
        request = self.context.get('request')
        user = request.user
        overtime, created = Overtime.objects.get_or_create(
            user=user,
            clock_date=today,
            payroll_period=payroll_period,
            defaults={
                'hours': validated_data['hours']
            }
        )
        if not created:
            overtime.hours = validated_data['hours']
            overtime.save()
        return overtime

    def update(self, instance, validated_data):
        instance.hours = validated_data.get('hours', instance.hours)
        instance.save()
        return instance

    def validate(self, data):
        hours = data.get('hours')
        if hours is None:
            raise serializers.ValidationError({"hours": "Field Hours is required"})
        if hours <= 0:
            raise serializers.ValidationError({"hours": "Field Hours must be greater than 0"})
        if hours > 3:
            raise serializers.ValidationError({"hours": "Field Hours maximal is 3 hours"})
        return data

from rest_framework import serializers
from ..models.payroll_period_model import PayrollPeriod


class PayrollPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPeriod
        fields = '__all__'

    def create(self, validated_data):
        return PayrollPeriod.objects.create(**validated_data)

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date is None:
            raise serializers.ValidationError({"start_date": "Field Start is required"})
        if end_date is None:
            raise serializers.ValidationError({"end_date": "Field End is required"})
        if start_date > end_date:
            raise serializers.ValidationError({"start_date": "Field Start must not be later than End date"})

        return data
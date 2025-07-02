from ..models.payroll_model import Payroll
from rest_framework import serializers

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ['id', 'payroll_period', 'user', 'basic_salary', 'salary_per_hour', 'attended_days', 'attended_percentage', 'overtime_hours', 'overtime_pay', 'reimbursement_amount', 'take_home_salary', 'created_at', 'updated_at']
        read_only_fields = ('id', 'user', 'payroll_period', 'created_at', 'updated_at')

    def validate(self, validated_data):
        basic_salary = validated_data.get('basic_salary')
        if basic_salary <= 0:
            raise serializers.ValidationError({"basic_salary": "Basic Salary must be greater than 0"})

        attended_days = validated_data.get('attended_days')
        if attended_days < 0:
            raise serializers.ValidationError({"attended_days": "Attended Days must be greater than 0"})
        elif attended_days > 30:
            raise serializers.ValidationError({"attended_days": "Attended Days must not be greater than 30"})

        attended_percentage = validated_data.get('attended_percentage')
        if attended_percentage < 0 or attended_percentage > 100:
            raise serializers.ValidationError({"attended_percentage": "Attended Percentage must be between 0 and 100"})

        overtime_hours = validated_data.get('overtime_hours')
        if overtime_hours < 0:
            raise serializers.ValidationError({"overtime_hours": "Overtime Hours must be greater than 0"})

        reimbursement_amount = validated_data.get('reimbursement_amount')
        if reimbursement_amount < 0:
            raise serializers.ValidationError({"reimbursement_amount": "Reimbursement Amount must be greater than 0"})

        take_home_salary = validated_data.get('take_home_salary')
        if take_home_salary < 0:
            raise serializers.ValidationError({"take_home_salary": "Take-Home Salary must be greater than 0"})

        return validated_data
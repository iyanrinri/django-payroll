from ..models.salary_model import Salary
from rest_framework import serializers

class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = ['id', 'amount', 'user', 'created_at', 'updated_at']
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0"})
        return value
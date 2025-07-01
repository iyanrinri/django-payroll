from ..models.salary_history_model import SalaryHistory
from rest_framework import serializers

class SalaryHistorySerializer(serializers.ModelSerializer):
    diff = serializers.SerializerMethodField()

    class Meta:
        model = SalaryHistory
        fields = ['id', 'amount', 'diff', 'user', 'created_at']
        read_only_fields = ('id', 'user', 'created_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0"})
        return value

    def get_diff(self, obj):
        all_histories = self.context.get('all_histories', [])
        print(all_histories)
        try:
            idx = all_histories.index(obj)
            if idx + 1 < len(all_histories):
                previous = all_histories[idx + 1]
                return obj.amount - previous.amount
        except ValueError:
            pass
        return None
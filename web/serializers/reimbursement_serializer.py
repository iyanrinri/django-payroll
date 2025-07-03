from rest_framework import serializers

from ..models.reimbursement_model import Reimbursement
from ..services.reimbursement_service import create_reimbursement_by_request, validate_data


class ReimbursementCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reimbursement
        fields = ['amount', 'claim_date', 'description']

    def create(self, validated_data):
        request = self.context.get('request')
        reimbursement = create_reimbursement_by_request(request, validated_data)
        return reimbursement

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.claim_date = validated_data.get('claim_date', instance.claim_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate(self, data):
        validate_data(data)
        return data

class ReimbursementSerializer(serializers.ModelSerializer):
    amount_display = serializers.SerializerMethodField()
    claim_date_display = serializers.SerializerMethodField()
    class Meta:
        model = Reimbursement
        fields = '__all__'

    def get_claim_date_display(self, obj):
        return obj.claim_date.strftime('%a, %d %B %Y')

    def get_amount_display(self, obj):
        amount = "{:,.2f}".format(obj.amount)
        return f"{amount}"

    def create(self, validated_data):
        request = self.context.get('request')
        reimbursement = create_reimbursement_by_request(request, validated_data)
        return reimbursement

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.claim_date = validated_data.get('claim_date', instance.claim_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate(self, data):
        validate_data(data)
        return data

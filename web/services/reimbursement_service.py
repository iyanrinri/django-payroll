from datetime import datetime, date

from rest_framework.exceptions import ValidationError

from web.models import Reimbursement
from web.services.payroll_period_service import get_payroll_period

def validate_data(data):
    amount = data.get('amount')
    if amount is None:
        raise ValidationError({"amount": "Field Amount is required"})
    if amount <= 0:
        raise ValidationError({"amount": "Field Amount must be greater than 0"})

    claim_date = data.get('claim_date')
    if claim_date is None:
        raise ValidationError({"claim_date": "Field claim_date is required"})
    if not isinstance(claim_date, date):
        raise ValidationError({"claim_date": "Field claim_date not valid format, use YYYY-MM-DD"})

    if isinstance(claim_date, str):
        try:
            datetime.strptime(claim_date.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValidationError({"claim_date": "Field claim_date not valid format, use YYYY-MM-DD"})
    elif not isinstance(claim_date, date):
        raise ValidationError({"claim_date": "Field claim_date must be a string in YYYY-MM-DD format or a valid date"})


def create_reimbursement_by_request(request, validated_data: dict):
    payroll_period = get_payroll_period()
    user = request.user
    reimbursement = Reimbursement.objects.create(
        user=user,
        claim_date=validated_data['claim_date'],
        payroll_period=payroll_period,
        amount=validated_data['amount'],
        description=validated_data['description']
    )

    return reimbursement

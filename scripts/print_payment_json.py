import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()

from booking.models import Payment, PaymentActionLog


def serialize_payment(p):
    if not p:
        return None
    try:
        from booking.serializers import PaymentSerializer
        return PaymentSerializer(p).data
    except Exception:
        from django.core import serializers
        # fallback to Django's serializer (returns list with one item)
        try:
            return json.loads(serializers.serialize('json', [p]))[0]
        except Exception:
            # last-resort manual dict
            return {
                'id': p.id,
                'organization_id': getattr(p.organization, 'id', None),
                'branch_id': getattr(p.branch, 'id', None),
                'amount': p.amount,
                'status': p.status,
                'transaction_number': p.transaction_number,
                'transaction_type': p.transaction_type,
                'date': str(p.date),
            }


if __name__ == '__main__':
    p = Payment.objects.first()
    print('--- PAYMENT_JSON ---')
    print(json.dumps(serialize_payment(p), indent=2, default=str))

    al = PaymentActionLog.objects.first()
    print('\n--- PAYMENT_ACTION_LOG_JSON ---')
    if al:
        d = {
            'id': al.id,
            'payment_id': al.payment_id,
            'action': al.action,
            'performed_by_id': getattr(al.performed_by, 'id', None),
            'details': al.details,
            'created_at': str(al.created_at),
        }
        print(json.dumps(d, indent=2, default=str))
    else:
        print('No PaymentActionLog found')

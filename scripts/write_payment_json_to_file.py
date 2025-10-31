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
        try:
            return json.loads(serializers.serialize('json', [p]))[0]
        except Exception:
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


def main():
    p = Payment.objects.first()
    al = PaymentActionLog.objects.first()
    out = {
        'payment': serialize_payment(p),
        'payment_action_log': None,
    }
    if al:
        out['payment_action_log'] = {
            'id': al.id,
            'payment_id': al.payment_id,
            'action': al.action,
            'performed_by_id': getattr(al.performed_by, 'id', None),
            'details': al.details,
            'created_at': str(al.created_at),
        }

    dst = os.path.join(os.getcwd(), 'payment_json_output.json')
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(out, f, default=str, indent=2)
    print('Wrote:', dst)

if __name__ == '__main__':
    main()

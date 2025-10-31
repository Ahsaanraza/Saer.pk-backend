import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()
from booking.models import Payment, PaymentActionLog
p = Payment.objects.first()
print('Payment id', p.id)
try:
    al = PaymentActionLog.objects.create(payment=p, action='test_log', performed_by=None, details={'msg':'test'})
    print('Created log id', al.id)
except Exception as e:
    print('Create log failed:', e)
    import traceback
    traceback.print_exc()

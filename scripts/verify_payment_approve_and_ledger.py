import os
import django
import json
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()

from booking.models import Payment, PaymentActionLog
from ledger.models import LedgerEntry, LedgerLine
from django.contrib.auth import get_user_model
User = get_user_model()

# Helper: pick an existing payment or create a minimal one
p = Payment.objects.first()
created = False
if not p:
    # Create a payment using existing org/branch/agency if available
    org = None
    br = None
    ag = None
    try:
        from organization.models import Organization, Branch, Agency
        org = Organization.objects.first()
        br = Branch.objects.filter(organization=org).first() if org else Branch.objects.first()
        ag = Agency.objects.filter(organization=org).first() if org else Agency.objects.first()
    except Exception:
        pass
    try:
        p = Payment.objects.create(
            organization=org,
            branch=br,
            agency=ag,
            method='cash',
            amount=1000.0,
            status='Pending'
        )
        created = True
    except Exception as e:
        print('Failed to create test Payment:', e)
        raise

print('Using Payment id:', p.id, 'status:', p.status)

# Approve the payment by setting status to Completed and saving
old_status = p.status
p.status = 'Completed'
p.save()
print('Payment saved with status:', p.status)

# Fetch ledger entries and action logs
entries = LedgerEntry.objects.filter(metadata__contains={'payment_id': p.id})
print('LedgerEntry count for payment:', entries.count())
for e in entries:
    print('Entry id:', e.id, 'metadata:', e.metadata)
    lines = LedgerLine.objects.filter(ledger_entry=e)
    for l in lines:
        print('  Line:', l.account_id, 'debit:', l.debit, 'credit:', l.credit, 'final_balance:', l.final_balance)

logs = PaymentActionLog.objects.filter(payment=p).order_by('-created_at')
print('PaymentActionLog count:', logs.count())
for l in logs:
    print('Log:', l.action, l.details, l.created_at)

# Print final balances of involved accounts (if any ledger lines exist)
if entries.exists():
    acct_ids = set()
    for l in LedgerLine.objects.filter(ledger_entry__in=entries):
        acct_ids.add(l.account_id)
    from ledger.models import Account
    for aid in acct_ids:
        a = Account.objects.filter(pk=aid).first()
        if a:
            print('Account', a.id, a.name, 'balance', a.balance)

# If we created a Payment for this test, optionally delete it (commented out)
# if created:
#     p.delete()

print('Done')

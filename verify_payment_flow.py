import os
import django
import json
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings')
django.setup()

from booking.models import Payment, PaymentActionLog
from ledger.models import LedgerEntry, LedgerLine, Account

# Pick an existing Payment or create a minimal one
p = Payment.objects.first()
created = False
if not p:
    try:
        from organization.models import Organization, Branch, Agency
        org = Organization.objects.first()
        br = Branch.objects.filter(organization=org).first() if org else Branch.objects.first()
        ag = Agency.objects.filter(organization=org).first() if org else Agency.objects.first()
    except Exception:
        org = br = ag = None
    p = Payment.objects.create(
        organization=org,
        branch=br,
        agency=ag,
        method='cash',
        amount=500.0,
        status='Pending',
    )
    created = True

print('Using Payment id:', p.id, 'initial status:', p.status)

# Approve the payment (set Completed) which should trigger ledger posting via signal
p.status = 'Completed'
p.save()
print('Payment saved with status:', p.status)

# Query ledger entries
entries = LedgerEntry.objects.filter(metadata__contains={'payment_id': p.id})
print('\nLedgerEntry count for payment:', entries.count())
for e in entries:
    print('Entry id:', e.id, 'metadata:', e.metadata)
    for l in LedgerLine.objects.filter(ledger_entry=e):
        print('  Line -> account:', l.account_id, 'debit:', l.debit, 'credit:', l.credit, 'final_balance:', l.final_balance)

# Payment action logs
logs = PaymentActionLog.objects.filter(payment=p).order_by('-created_at')
print('\nPaymentActionLog count:', logs.count())
for l in logs:
    print('Log:', l.action, l.details, l.created_at)

# Account balances for involved accounts
acct_ids = set()
for l in LedgerLine.objects.filter(ledger_entry__in=entries):
    acct_ids.add(l.account_id)
print('\nInvolved accounts and balances:')
for aid in acct_ids:
    a = Account.objects.filter(pk=aid).first()
    if a:
        print('Account', a.id, a.name, 'balance', a.balance)

print('\nDone')

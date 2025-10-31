from django.test import TestCase
from django.core.management import call_command
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User

from organization.models import Organization, Branch, Agency
from booking.models import Booking, Payment, PaymentActionLog
from ledger.models import LedgerEntry, LedgerLine


class PaymentLedgerIntegrationTests(TestCase):
    def setUp(self):
        # basic org/branch/user setup
        self.user = User.objects.create(username='tester')
        self.org = Organization.objects.create(name='OrgTest')
        self.branch = Branch.objects.create(organization=self.org, name='BranchTest')
        self.agency = Agency.objects.create(branch=self.branch, name='AgencyTest')

        # simple booking
        self.booking = Booking.objects.create(
            user=self.user,
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            booking_number='BKG-TEST-1',
            status='New'
        )

        # Prepare a lightweight 'item' that posting logic can consume without creating heavy Hotel/Ticket objects
        self.owner_org = Organization.objects.create(name='OwnerOrg')
        self.mock_item = SimpleNamespace(
            total_price=1000,
            price=1000,
            is_price_pkr=True,
            inventory_owner_organization=self.owner_org,
            inventory_owner_organization_id=self.owner_org.id,
        )

    def _attach_mock_items(self, booking):
        # Override the related manager on the instance so signals will find our mock items
        booking.hotel_details = SimpleNamespace(all=lambda: [self.mock_item])
        booking.transport_details = SimpleNamespace(all=lambda: [])
        booking.ticket_details = SimpleNamespace(all=lambda: [])

    def test_approve_creates_ledger_and_action_log(self):
        # create a payment that will be approved
        payment = Payment.objects.create(
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            agent=self.user,
            booking=self.booking,
            method='cash',
            amount=1000,
            status='Pending'
        )

        # attach mock items so auto_post_payment has data to post
        self._attach_mock_items(self.booking)

        # Approve (= set status Completed) which triggers the post_save signal
        payment.status = 'Completed'
        payment.save()

        # Find ledger entry created for this payment
        entries = [e for e in LedgerEntry.objects.all() if isinstance(e.metadata, dict) and e.metadata.get('payment_id') == payment.id]
        self.assertTrue(entries, "LedgerEntry for payment not created")
        entry = entries[0]

        # Ensure two ledger lines (debit + credit)
        lines = list(entry.lines.all())
        self.assertEqual(len(lines), 2)
        debits = [l for l in lines if l.debit and l.debit > 0]
        credits = [l for l in lines if l.credit and l.credit > 0]
        self.assertTrue(debits and credits, "Entry must have one debit and one credit")

        # Ensure PaymentActionLog created with ledger_entry_created action
        pal = PaymentActionLog.objects.filter(payment=payment, action='ledger_entry_created').first()
        self.assertIsNotNone(pal, "PaymentActionLog with action 'ledger_entry_created' not found")

    def test_posting_failure_creates_payment_post_failed_log(self):
        # Create payment and attach mock item
        payment = Payment.objects.create(
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            agent=self.user,
            booking=self.booking,
            method='cash',
            amount=2000,
            status='Pending'
        )
        self._attach_mock_items(self.booking)

        # Patch LedgerLine.objects.create to raise during posting to simulate failure
        with patch('ledger.models.LedgerLine.objects.create', side_effect=Exception('simulated failure')):
            with self.assertRaises(Exception):
                payment.status = 'Completed'
                payment.save()

        # After failure the signal attempts to write a PaymentActionLog with action 'payment_post_failed'
        pal = PaymentActionLog.objects.filter(payment=payment, action='payment_post_failed').first()
        self.assertIsNotNone(pal, "PaymentActionLog with action 'payment_post_failed' not created on posting failure")

    def test_reconcile_command_posts_missing_ledgers(self):
        # Create a payment via bulk_create to simulate missed signal
        p = Payment(
            organization=self.org,
            branch=self.branch,
            agency=self.agency,
            agent=self.user,
            booking=self.booking,
            method='cash',
            amount=1500,
            status='Completed',
        )
        Payment.objects.bulk_create([p])

        # reload payment from DB
        payment = Payment.objects.order_by('-id').first()

        # Patch the posting handler so it will see our mock items and create a ledger entry
        def fake_auto_post(sender, instance, created=False, **kwargs):
            # create a simple ledger entry for the payment
            entry = LedgerEntry.objects.create(
                booking_no=(instance.booking.booking_number if instance.booking else None),
                service_type='payment',
                narration=f'Posted by reconcile for payment {instance.id}',
                metadata={'payment_id': instance.id}
            )
            # create two lines (debit + credit)
            LedgerLine.objects.create(ledger_entry=entry, account=None, debit=instance.amount or 0, credit=0, final_balance=0)
            LedgerLine.objects.create(ledger_entry=entry, account=None, debit=0, credit=instance.amount or 0, final_balance=0)

        # Call reconcile with patched auto_post to actually post
        with patch('booking.management.commands.reconcile_payments.auto_post_payment', side_effect=fake_auto_post):
            call_command('reconcile_payments', '--apply')

        # Verify ledger entry exists for the payment
        entries = [e for e in LedgerEntry.objects.all() if isinstance(e.metadata, dict) and e.metadata.get('payment_id') == payment.id]
        self.assertTrue(entries, "Reconcile did not create a LedgerEntry for the payment")

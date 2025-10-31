from django.core.management.base import BaseCommand
from django.db import transaction
from booking.models import Payment
from ledger.models import LedgerEntry
from ledger.signals import auto_post_payment


class Command(BaseCommand):
    help = "Reconcile payments by creating ledger entries for payments missing them.\n
    By default this is a dry-run. Use --apply to actually invoke posting."

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Actually post ledger entries. Otherwise just list.')
        parser.add_argument('--limit', type=int, default=0, help='Limit number of payments to process (0 = no limit)')

    def handle(self, *args, **options):
        apply = options.get('apply', False)
        limit = options.get('limit', 0)

        self.stdout.write("Scanning for completed payments missing ledger entries...")

        qs = Payment.objects.filter(status__in=["Completed", "approved", "Approved"])  # check common casings

        count = 0
        to_process = []
        for p in qs.order_by('id'):
            try:
                # idempotency check: ledger entry with metadata.payment_id == p.id
                exists = LedgerEntry.objects.filter(metadata__contains={"payment_id": p.id}).exists()
            except Exception:
                # fallback: scan entries and check metadata attribute if DB doesn't support JSON lookup
                exists = any(e for e in LedgerEntry.objects.all() if isinstance(e.metadata, dict) and e.metadata.get('payment_id') == p.id)

            if not exists:
                to_process.append(p)
                count += 1
                if limit and count >= limit:
                    break

        if not to_process:
            self.stdout.write(self.style.SUCCESS('No payments need reconciliation.'))
            return

        self.stdout.write(f"Found {len(to_process)} payments missing ledger entries.")
        for p in to_process:
            self.stdout.write(f"- Payment id={p.id} booking={getattr(p.booking, 'booking_number', None)} amount={p.amount} org={getattr(p.organization, 'id', None)} status={p.status}")

        if not apply:
            self.stdout.write(self.style.WARNING("Dry-run complete. Re-run with --apply to post ledger entries."))
            return

        self.stdout.write(self.style.NOTICE("Applying reconciliation now (this will invoke ledger posting for each payment)..."))
        processed = 0
        for p in to_process:
            try:
                # Use the Payment model's post_to_ledger method which centralizes posting logic.
                with transaction.atomic():
                    if hasattr(p, 'post_to_ledger') and callable(getattr(p, 'post_to_ledger')):
                        p.post_to_ledger()
                    else:
                        # fallback to calling the signal handler if method not present
                        from ledger.signals import auto_post_payment
                        auto_post_payment(sender=Payment, instance=p, created=False)
                processed += 1
                self.stdout.write(self.style.SUCCESS(f"Posted ledger for Payment id={p.id}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to post for Payment id={p.id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Reconciliation complete. Posted {processed} payments."))

from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from ledger.models import LedgerEntry, LedgerLine, Account
from .models import TransactionJournal, AuditLog
from ledger.currency_utils import convert_sar_to_pkr
from booking.models import Booking
from .models import FinancialRecord, Expense
from django.db.models import Sum


def post_journal_to_ledger(journal: TransactionJournal, actor=None):
    """
    Post a TransactionJournal into the ledger as a LedgerEntry with LedgerLines.
    Expects journal.entries as a list of dicts: {'account_id': int, 'debit': Decimal, 'credit': Decimal}
    Returns the created LedgerEntry or raises ValueError on invalid input.
    """
    if journal.posted:
        raise ValueError("Journal already posted")

    entries = journal.entries or []
    if not entries:
        raise ValueError("Journal has no entries")

    # Validate accounts exist
    account_ids = [e.get("account_id") for e in entries if e.get("account_id")]
    if not account_ids:
        raise ValueError("Entries must contain 'account_id' fields")

    accounts = Account.objects.select_for_update().filter(pk__in=account_ids)
    account_map = {a.id: a for a in accounts}

    # Create LedgerEntry + lines atomically
    with transaction.atomic():
        # Re-select accounts with locks
        Account.objects.select_for_update().filter(pk__in=account_ids)

        ledger_entry = LedgerEntry.objects.create(
            booking_no=journal.reference,
            service_type="other",
            narration=journal.narration,
            created_by=journal.created_by,
            creation_datetime=timezone.now(),
            metadata={"journal_id": journal.id},
            internal_notes=[f"Posted from TransactionJournal {journal.id} by user {actor.id if actor else 'system'}"],
        )

        # apply each line and update account balances
        for ent in entries:
            acc_id = ent.get("account_id")
            debit = Decimal(str(ent.get("debit" or 0))) if ent.get("debit") else Decimal("0.00")
            credit = Decimal(str(ent.get("credit" or 0))) if ent.get("credit") else Decimal("0.00")

            if acc_id not in account_map:
                raise ValueError(f"Account {acc_id} not found for journal posting")

            account = account_map[acc_id]

            # update account balance: balance = balance + debit - credit
            account.balance = account.balance + debit - credit
            account.save()

            LedgerLine.objects.create(
                ledger_entry=ledger_entry,
                account=account,
                debit=debit,
                credit=credit,
                final_balance=account.balance,
            )

        journal.ledger_entry_id = ledger_entry.id
        journal.posted = True
        journal.save()

        # Audit log
        try:
            AuditLog.objects.create(
                actor=actor,
                action="post",
                object_type="TransactionJournal",
                object_id=str(journal.id),
                before=None,
                after={"posted": True, "ledger_entry_id": ledger_entry.id},
                reason="Auto-post from expense creation",
            )
        except Exception:
            # non-fatal
            pass

    return ledger_entry


def calculate_profit_loss(booking_id: int):
    """Calculate and persist FinancialRecord for a booking.

    Simple logic:
    - income_amount: use booking.total_in_pkr if set, else booking.total_amount
    - purchase_cost: sum of item costs (hotel, transport, ticket) converted to PKR where needed
    - expenses_amount: sum of Expense entries linked to booking
    - profit_loss = income - purchase_cost - expenses
    """
    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        return None

    # income
    income = Decimal(str(getattr(booking, 'total_in_pkr', None) or getattr(booking, 'total_amount', 0) or 0))

    # purchase cost calculation from booking details
    purchase = Decimal("0.00")

    # hotels
    for h in getattr(booking, 'hotel_details', []).all():
        amt = getattr(h, 'total_in_pkr', None) if getattr(h, 'total_in_pkr', None) is not None else getattr(h, 'total_price', 0)
        if not getattr(h, 'is_price_pkr', True) and getattr(h, 'inventory_owner_organization', None):
            try:
                amt = Decimal(str(convert_sar_to_pkr(amt, h.inventory_owner_organization)))
            except Exception:
                amt = Decimal(str(amt))
        purchase += Decimal(str(amt or 0))

    # transport
    for t in getattr(booking, 'transport_details', []).all():
        amt = getattr(t, 'price_in_pkr', None) if getattr(t, 'price_in_pkr', None) is not None else getattr(t, 'price', 0)
        if not getattr(t, 'is_price_pkr', True) and getattr(t, 'inventory_owner_organization', None):
            try:
                amt = Decimal(str(convert_sar_to_pkr(amt, t.inventory_owner_organization)))
            except Exception:
                amt = Decimal(str(amt))
        purchase += Decimal(str(amt or 0))

    # tickets
    for tk in getattr(booking, 'ticket_details', []).all():
        seats = getattr(tk, 'seats', 0) or 0
        price = getattr(tk, 'adult_price', None) if getattr(tk, 'adult_price', None) is not None else getattr(tk, 'adult_price', 0)
        amt = Decimal(str((price or 0) * seats))
        purchase += amt

    # expenses linked to booking
    exp_qs = Expense.objects.filter(booking_id=booking_id)
    expenses_sum = exp_qs.aggregate(total=Sum('amount'))['total'] or 0
    # convert any SAR expenses — assume Expense.currency set
    expenses_total = Decimal('0.00')
    for e in exp_qs:
        if e.currency and e.currency.upper() == 'SAR':
            try:
                amt = Decimal(str(convert_sar_to_pkr(e.amount, e.organization)))
            except Exception:
                amt = Decimal(str(e.amount))
        else:
            amt = Decimal(str(e.amount))
        expenses_total += amt

    profit = income - purchase - expenses_total

    fr, created = FinancialRecord.objects.update_or_create(
        booking_id=booking_id,
        defaults={
            'organization': booking.organization,
            'branch': booking.branch,
            'service_type': getattr(booking, 'booking_type', 'other').lower(),
            'income_amount': income,
            'purchase_cost': purchase,
            'expenses_amount': expenses_total,
            'profit_loss': profit,
            'currency': 'PKR',
            'metadata': {
                'booking_number': booking.booking_number,
                'linked_booking_id': getattr(booking, 'linked_booking_id', None)
            },
        }
    )

    return fr


def aggregate_financials_for_booking(booking_id: int):
    """Return aggregated totals for a booking including any FinancialRecords
    whose metadata.linked_booking_id references this booking.

    Returns a dict: { income_amount, purchase_cost, expenses_amount, profit_loss, count }
    This is a read-time aggregation only and does not modify persisted FinancialRecords.
    """
    from django.db.models import Sum
    qs_main = FinancialRecord.objects.filter(booking_id=booking_id)
    # FRs for walk-ins may reference linked_booking_id in metadata
    qs_linked = FinancialRecord.objects.filter(metadata__linked_booking_id=booking_id)

    agg_main = qs_main.aggregate(
        income=Sum('income_amount'),
        purchase=Sum('purchase_cost'),
        expenses=Sum('expenses_amount'),
        profit=Sum('profit_loss')
    )
    agg_linked = qs_linked.aggregate(
        income=Sum('income_amount'),
        purchase=Sum('purchase_cost'),
        expenses=Sum('expenses_amount'),
        profit=Sum('profit_loss')
    )

    def _val(d, k):
        v = d.get(k) if d else None
        return v or 0

    income = _val(agg_main, 'income') + _val(agg_linked, 'income')
    purchase = _val(agg_main, 'purchase') + _val(agg_linked, 'purchase')
    expenses = _val(agg_main, 'expenses') + _val(agg_linked, 'expenses')
    profit = _val(agg_main, 'profit') + _val(agg_linked, 'profit')

    count = qs_main.count() + qs_linked.count()

    return {
        'income_amount': income,
        'purchase_cost': purchase,
        'expenses_amount': expenses,
        'profit_loss': profit,
        'count': count,
    }

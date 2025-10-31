from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .models import Account, LedgerEntry, LedgerLine
from .serializers import LedgerEntrySerializer
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from organization.models import Organization, Branch, Agency
from .models import Account
from django.db import models
from django.conf import settings

class LedgerCreateAPIView(APIView):
    """Create a simple two-line ledger entry (debit & credit)."""

    def post(self, request):
        data = request.data
        debit_account_id = data.get("debit_account_id")
        credit_account_id = data.get("credit_account_id")
        amount = data.get("amount")
        booking_no = data.get("booking_no")
        service_type = data.get("service_type")
        narration = data.get("narration")
        metadata = data.get("metadata") or {}

        if not (debit_account_id and credit_account_id and amount):
            return Response({"detail": "debit_account_id, credit_account_id and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(str(amount))
        except Exception:
            return Response({"detail": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        debit_account = get_object_or_404(Account, pk=debit_account_id)
        credit_account = get_object_or_404(Account, pk=credit_account_id)

        # create entry and update balances atomically
        with transaction.atomic():
            # lock accounts
            locked_accounts = Account.objects.select_for_update().filter(pk__in=[debit_account.id, credit_account.id])
            audit_note = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Created via API by user {request.user.id if request.user.is_authenticated else 'unknown'}."
            entry = LedgerEntry.objects.create(
                booking_no=booking_no,
                service_type=service_type or "other",
                narration=narration,
                metadata=metadata,
                internal_notes=[audit_note],
            )

            # debit increases balance (for asset style accounts) and credit decreases; business logic may vary
            # Here we treat balance as a net asset: balance = balance + debit - credit

            # create debit line
            debit_final = (debit_account.balance + amount)
            debit_line = LedgerLine.objects.create(
                ledger_entry=entry,
                account=debit_account,
                debit=amount,
                credit=Decimal("0.00"),
                final_balance=debit_final,
            )
            debit_account.balance = debit_final
            debit_account.save()

            # create credit line
            credit_final = (credit_account.balance - amount)
            credit_line = LedgerLine.objects.create(
                ledger_entry=entry,
                account=credit_account,
                debit=Decimal("0.00"),
                credit=amount,
                final_balance=credit_final,
            )
            credit_account.balance = credit_final
            credit_account.save()

        serializer = LedgerEntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# --- Pending/Final Balance Endpoints ---
@api_view(["GET"])
def agents_pending_balances(request):
    """Return pending/final balances for all agent accounts."""
    if getattr(settings, "USE_DUMMY_DATA", False):
        data = [
            {"id": 1, "name": "Agent A", "agency_id": 10, "balance": 5000},
            {"id": 2, "name": "Agent B", "agency_id": 11, "balance": 3000},
        ]
        return Response(data)
    agents = Account.objects.filter(account_type="AGENT")
    data = [
        {
            "id": acc.id,
            "name": acc.name,
            "agency_id": acc.agency_id,
            "balance": acc.balance,
        }
        for acc in agents
    ]
    return Response(data)

@api_view(["GET"])
def area_agents_pending_balances(request):
    """Return pending/final balances for all area agent accounts (customize filter as needed)."""
    if getattr(settings, "USE_DUMMY_DATA", False):
        data = [
            {"id": 3, "name": "Area Agent X", "agency_id": 20, "balance": 7000},
            {"id": 4, "name": "Area Agent Y", "agency_id": 21, "balance": 2000},
        ]
        return Response(data)
    area_agents = Account.objects.filter(account_type="AGENT")
    data = [
        {
            "id": acc.id,
            "name": acc.name,
            "agency_id": acc.agency_id,
            "balance": acc.balance,
        }
        for acc in area_agents
    ]
    return Response(data)

@api_view(["GET"])
def branch_pending_balances(request):
    """Return pending/final balances for all branch accounts."""
    if getattr(settings, "USE_DUMMY_DATA", False):
        data = [
            {"branch_id": 1, "branch_name": "Main Branch", "total_balance": 10000},
            {"branch_id": 2, "branch_name": "Sub Branch", "total_balance": 4000},
        ]
        return Response(data)
    branches = Branch.objects.all()
    data = []
    for branch in branches:
        branch_accounts = Account.objects.filter(branch=branch)
        total_balance = sum(acc.balance for acc in branch_accounts)
        data.append({
            "branch_id": branch.id,
            "branch_name": branch.name,
            "total_balance": total_balance,
        })
    return Response(data)

@api_view(["GET"])
def organization_pending_balances(request):
    """Return pending/final balances for all organization accounts."""
    if getattr(settings, "USE_DUMMY_DATA", False):
        data = [
            {"organization_id": 1, "organization_name": "Org Alpha", "total_balance": 25000},
            {"organization_id": 2, "organization_name": "Org Beta", "total_balance": 8000},
        ]
        return Response(data)
    orgs = Organization.objects.all()
    data = []
    for org in orgs:
        org_accounts = Account.objects.filter(organization=org)
        total_balance = sum(acc.balance for acc in org_accounts)
        data.append({
            "organization_id": org.id,
            "organization_name": org.name,
            "total_balance": total_balance,
        })
    return Response(data)

@api_view(["GET"])
def final_balance(request):
    """Return the global final balance (sum of all account balances)."""
    if getattr(settings, "USE_DUMMY_DATA", False):
        return Response({"final_balance": 99999})
    total = Account.objects.all().aggregate(total=models.Sum("balance"))["total"] or 0
    return Response({"final_balance": total})

class LedgerListAPIView(APIView):
    def get(self, request):
        qs = LedgerEntry.objects.all().order_by("-creation_datetime")
        # simple pagination could be added later
        serializer = LedgerEntrySerializer(qs, many=True)
        return Response(serializer.data)


class LedgerReverseAPIView(APIView):
    def post(self, request, pk):
        entry = get_object_or_404(LedgerEntry, pk=pk)
        if entry.reversed:
            return Response({"detail": "Entry already reversed."}, status=status.HTTP_400_BAD_REQUEST)

        # create reversing entry: swap debit/credit for each line
        with transaction.atomic():
            # lock all involved accounts
            account_ids = list(entry.lines.values_list("account_id", flat=True))
            Account.objects.select_for_update().filter(pk__in=account_ids)

            reverse_entry = LedgerEntry.objects.create(
                booking_no=entry.booking_no,
                service_type=entry.service_type,
                narration=(f"Reversal of #{entry.id}: " + (entry.narration or "")),
                metadata={"reversed_of": entry.id},
                reversed_of=entry,
            )

            for line in entry.lines.all():
                # create opposite line
                rev_debit = line.credit
                rev_credit = line.debit

                account = line.account
                # apply reversal to balances
                account.balance = account.balance + rev_debit - rev_credit
                account.save()

                LedgerLine.objects.create(
                    ledger_entry=reverse_entry,
                    account=account,
                    debit=rev_debit,
                    credit=rev_credit,
                    final_balance=account.balance,
                )

            entry.reversed = True
            entry.save()

        serializer = LedgerEntrySerializer(reverse_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

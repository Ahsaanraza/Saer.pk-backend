from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

from organization.models import Organization, Branch, Agency


class Account(models.Model):

    @property
    def total_debit(self):
        return self.lines.aggregate(total=models.Sum('debit'))['total'] or Decimal('0.00')

    @property
    def total_credit(self):
        return self.lines.aggregate(total=models.Sum('credit'))['total'] or Decimal('0.00')

    @property
    def final_balance_calc(self):
        # This is always total_debit - total_credit
        return self.total_debit - self.total_credit
    ACCOUNT_TYPE_CHOICES = [
        ("CASH", "Cash"),
        ("BANK", "Bank"),
        ("RECEIVABLE", "Receivable"),
        ("PAYABLE", "Payable"),
        ("AGENT", "Agent"),
        ("SALES", "Sales"),
        ("COMMISSION", "Commission"),
        ("SUSPENSE", "Suspense"),
    ]

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="accounts", blank=True, null=True
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="accounts", blank=True, null=True
    )
    agency = models.ForeignKey(
        Agency, on_delete=models.CASCADE, related_name="accounts", blank=True, null=True
    )
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, default="CASH")
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        scope = self.organization.name if self.organization else (self.branch.name if self.branch else (self.agency.name if self.agency else "Global"))
        return f"{self.name} ({self.account_type}) - {scope}"


class LedgerEntry(models.Model):
    SERVICE_TYPES = [
        ("ticket", "Ticket"),
        ("umrah", "Umrah"),
        ("hotel", "Hotel"),
        ("transport", "Transport"),
        ("package", "Package"),
        ("payment", "Payment"),
        ("refund", "Refund"),
        ("commission", "Commission"),
        ("other", "Other"),
    ]

    booking_no = models.CharField(max_length=255, blank=True, null=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, default="other")
    narration = models.TextField(blank=True, null=True)
    transaction_type = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    creation_datetime = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)
    reversed = models.BooleanField(default=False)
    reversed_of = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, related_name="reversals"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Internal notes for audit trail
    internal_notes = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"LedgerEntry #{self.id} - {self.booking_no or 'NoBooking'} - {self.creation_datetime}"


class LedgerLine(models.Model):
    ledger_entry = models.ForeignKey(LedgerEntry, on_delete=models.CASCADE, related_name="lines")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="lines")
    debit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"))
    credit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"))
    final_balance = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Line {self.id}: {self.account} - D:{self.debit} C:{self.credit} -> Bal:{self.final_balance}"

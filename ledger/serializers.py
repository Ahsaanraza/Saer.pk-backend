from rest_framework import serializers
from .models import Account, LedgerEntry, LedgerLine


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name", "account_type", "organization", "branch", "agency", "balance"]


class LedgerLineSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    account_id = serializers.IntegerField(source="account.id", read_only=True)
    account_name = serializers.CharField(source="account.name", read_only=True)

    class Meta:
        model = LedgerLine
        fields = [
            "id",
            "account",
            "account_id",
            "account_name",
            "debit",
            "credit",
            "final_balance",
            "created_at",
        ]


class LedgerEntrySerializer(serializers.ModelSerializer):
    lines = LedgerLineSerializer(many=True, read_only=True)

    class Meta:
        model = LedgerEntry
        fields = [
            "id",
            "booking_no",
            "service_type",
            "narration",
            "creation_datetime",
            "metadata",
            "reversed",
            "reversed_of",
            "lines",
            "created_at",
            "internal_notes",  # Expose internal_notes for audit trail
        ]

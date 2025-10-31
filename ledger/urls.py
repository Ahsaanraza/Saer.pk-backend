from django.urls import path
from .views import LedgerCreateAPIView, LedgerListAPIView, LedgerReverseAPIView
from .views import (
    LedgerCreateAPIView, LedgerListAPIView, LedgerReverseAPIView,
    agents_pending_balances, area_agents_pending_balances, branch_pending_balances, organization_pending_balances, final_balance
)

urlpatterns = [
    path("api/ledger/create/", LedgerCreateAPIView.as_view(), name="ledger-create"),
    path("api/ledger/list/", LedgerListAPIView.as_view(), name="ledger-list"),
    path("api/ledger/reverse/<int:pk>/", LedgerReverseAPIView.as_view(), name="ledger-reverse"),

    # Pending/final balance endpoints
    path("api/agents/pending-balances", agents_pending_balances, name="agents-pending-balances"),
    path("api/area-agents/pending-balances", area_agents_pending_balances, name="area-agents-pending-balances"),
    path("api/branch/pending-balances", branch_pending_balances, name="branch-pending-balances"),
    path("api/organization/pending-balances", organization_pending_balances, name="organization-pending-balances"),
    path("api/final-balance", final_balance, name="final-balance"),
]

from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("api/finance/expense/add", views.add_expense, name="expense-add"),
    path("api/finance/expense/list", views.list_expenses, name="expense-list"),
    path("api/finance/summary/all", views.summary_all, name="summary-all"),
    path("api/finance/manual/post", views.manual_posting, name="manual-post"),
    path("api/finance/ledger/by-service", views.ledger_by_service, name="ledger-by-service"),
    path("reports/profit-loss", views.report_profit_loss, name="report-profit-loss"),
    path("reports/fbr/summary", views.report_fbr_summary, name="report-fbr-summary"),
    path("reports/profit-loss/csv", views.report_profit_loss_csv, name="report-profit-loss-csv"),
    path("reports/fbr/summary/csv", views.report_fbr_summary_csv, name="report-fbr-summary-csv"),
    path("api/finance/dashboard/period", views.dashboard_period, name="dashboard-period"),
    path("api/finance/dashboard", views.compact_dashboard, name="dashboard-compact"),
]

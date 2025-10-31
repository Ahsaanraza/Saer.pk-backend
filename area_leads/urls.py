from django.urls import path
from .views import (
    AreaLeadCreateView,
    AreaLeadSearchView,
    FollowUpCreateView,
    FollowUpTodayView,
    ConversationAddView,
    ConversationHistoryView,
    PaymentPromiseAddView,
    PaymentPromiseUpcomingView,
    update_status,
)

urlpatterns = [
    path("create", AreaLeadCreateView.as_view(), name="area-leads-create"),
    path("search", AreaLeadSearchView.as_view(), name="area-leads-search"),
    path("followup/create", FollowUpCreateView.as_view(), name="area-leads-followup-create"),
    path("followup/today", FollowUpTodayView.as_view(), name="area-leads-followup-today"),
    path("conversation/add", ConversationAddView.as_view(), name="area-leads-conversation-add"),
    path("conversation/history", ConversationHistoryView.as_view(), name="area-leads-conversation-history"),
    path("payment-promise/add", PaymentPromiseAddView.as_view(), name="area-leads-payment-promise-add"),
    path("payment-promise/upcoming", PaymentPromiseUpcomingView.as_view(), name="area-leads-payment-promise-upcoming"),
    path("update-status", update_status, name="area-leads-update-status"),
]

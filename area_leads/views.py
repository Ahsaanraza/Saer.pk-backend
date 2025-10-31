from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import AreaLead, LeadFollowUp, LeadConversation, LeadPaymentPromise
from .serializers import (
    AreaLeadSerializer,
    LeadFollowUpSerializer,
    LeadConversationSerializer,
    LeadPaymentPromiseSerializer,
)
from .permissions import IsBranchUser


class AreaLeadCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsBranchUser]
    serializer_class = AreaLeadSerializer


class AreaLeadSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AreaLeadSerializer

    def get_queryset(self):
        passport = self.request.query_params.get("passport")
        contact = self.request.query_params.get("contact")
        qs = AreaLead.objects.all()
        if passport:
            qs = qs.filter(passport_number__iexact=passport)
        if contact:
            qs = qs.filter(contact_number__icontains=contact)
        return qs


class FollowUpCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsBranchUser]
    serializer_class = LeadFollowUpSerializer


class FollowUpTodayView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBranchUser]
    serializer_class = AreaLeadSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return AreaLead.objects.filter(followups__next_followup_date=today).distinct()


class ConversationAddView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsBranchUser]
    serializer_class = LeadConversationSerializer


class ConversationHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeadConversationSerializer

    def get_queryset(self):
        lead_id = self.request.query_params.get("lead_id")
        qs = LeadConversation.objects.all()
        if lead_id:
            qs = qs.filter(lead_id=lead_id)
        return qs.order_by("-timestamp")


class PaymentPromiseAddView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsBranchUser]
    serializer_class = LeadPaymentPromiseSerializer


class PaymentPromiseUpcomingView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsBranchUser]
    serializer_class = LeadPaymentPromiseSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return LeadPaymentPromise.objects.filter(due_date__gte=today).order_by("due_date")


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsBranchUser])
def update_status(request):
    lead_id = request.data.get("lead_id")
    status = request.data.get("status")
    lead = get_object_or_404(AreaLead, pk=lead_id)
    if status not in [choice[0] for choice in AreaLead._meta.get_field("lead_status").choices]:
        return Response({"error": "Invalid status"}, status=400)
    lead.lead_status = status
    lead.save(update_fields=["lead_status", "updated_at"])
    return Response({"message": "Lead status updated", "lead_id": lead.id})

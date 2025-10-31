from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Customer, Lead, FollowUpHistory, LoanCommitment
from .serializers import (
    CustomerSerializer,
    LeadSerializer,
    FollowUpHistorySerializer,
    LoanCommitmentSerializer,
)
from booking.models import Booking
from django.db import transaction
from django.utils import timezone


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(is_active=True).order_by("-updated_at")
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=["get", "post"], permission_classes=[IsAuthenticated])
    def auto_collection(self, request):
        """GET: return merged customer list (de-duplicated by phone/email).
           POST: trigger an on-demand scan of recent Bookings (same behavior as before)
        """
        if request.method == "GET":
            # merged listing: prefer grouping by phone then email
            qs = Customer.objects.filter(is_active=True).order_by("-updated_at")
            seen = {}
            merged = []
            for c in qs:
                key = None
                if c.phone:
                    key = f"phone:{c.phone}"
                elif c.email:
                    key = f"email:{c.email}"
                else:
                    key = f"id:{c.id}"

                existing = seen.get(key)
                if not existing:
                    seen[key] = c
                    merged.append(c)
                else:
                    # keep the one with latest updated_at
                    if c.updated_at and existing.updated_at and c.updated_at > existing.updated_at:
                        seen[key] = c
            serializer = CustomerSerializer(merged, many=True)
            return Response({"total_customers": len(merged), "customers": serializer.data})

        # POST behavior: scan recent bookings and upsert
        cutoff_days = int(request.data.get("cutoff_days", 30))
        since = timezone.now() - timezone.timedelta(days=cutoff_days)
        bookings = Booking.objects.filter(created_at__gte=since)
        created = 0
        updated = 0
        with transaction.atomic():
            for b in bookings:
                # Extract primary contact from booking person details
                person = None
                try:
                    person = b.person_details.first()
                except Exception:
                    person = None

                if not person:
                    continue

                full_name = " ".join(filter(None, [person.first_name, person.last_name])).strip() or b.user.username
                phone = person.contact_number or None
                email = None

                if not (phone or email):
                    continue

                obj, created_flag = Customer.objects.update_or_create(
                    phone=phone,
                    defaults={
                        "full_name": full_name,
                        "email": email,
                        "branch": b.branch,
                        "organization": b.organization,
                        "source": "Booking",
                        "last_activity": b.date,
                        "is_active": True,
                    },
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

        return Response({"created": created, "updated": updated})

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated], url_path="manual-add")
    def manual_add(self, request):
        """Create a customer manually via API."""
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(CustomerSerializer(obj).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Soft-delete: set is_active=False instead of hard delete."""
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]


class FollowUpViewSet(viewsets.ModelViewSet):
    queryset = FollowUpHistory.objects.all().order_by("-created_at")
    serializer_class = FollowUpHistorySerializer
    permission_classes = [IsAuthenticated]


class LoanCommitmentViewSet(viewsets.ModelViewSet):
    queryset = LoanCommitment.objects.all().order_by("-created_at")
    serializer_class = LoanCommitmentSerializer
    permission_classes = [IsAuthenticated]

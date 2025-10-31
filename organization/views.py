from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.views import APIView

from .models import Organization, Branch, Agency, OrganizationLink, AgencyProfile
from .serializers import (
    OrganizationSerializer,
    BranchSerializer,
    AgencySerializer,
    OrganizationLinkSerializer,
    AgencyProfileSerializer,
)
from .models import Rule
from .serializers import RuleSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsOrgStaff
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.db.utils import NotSupportedError
from django.db import transaction
from django.db.models import Sum
from .serializers import WalkInBookingSerializer
from .models import WalkInBooking
from tickets.models import HotelRooms, Hotels
from decimal import Decimal
from datetime import datetime


def _user_belongs_to_org(user, org_id):
    try:
        org_id_int = int(org_id)
    except Exception:
        return False
    if user.is_superuser:
        return True
    return any(o.id == org_id_int for o in user.organizations.all())


class OrganizationLinkViewSet(viewsets.ModelViewSet):
    """
    Manage linking between organizations.
    - Only Super Admins can create link requests.
    - Both organizations must accept for request_status to become True.
    - Either side can reject.
    """
    serializer_class = OrganizationLinkSerializer
    queryset = OrganizationLink.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Allow filtering links by organization_id"""
        organization_id = self.request.query_params.get("organization_id")
        queryset = self.queryset
        if organization_id:
            queryset = queryset.filter(
                Q(main_organization_id=organization_id) |
                Q(link_organization_id=organization_id)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        """Only Super Admin can create new organization link"""
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only Super Admins can create organization links."},
                status=status.HTTP_403_FORBIDDEN,
            )

        main_org_id = request.data.get("Main_organization_id")
        link_org_id = request.data.get("Link_organization_id")

        if not (main_org_id and link_org_id):
            return Response(
                {"detail": "Both Main_organization_id and Link_organization_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            main_org = Organization.objects.get(id=main_org_id)
            link_org = Organization.objects.get(id=link_org_id)
        except Organization.DoesNotExist:
            return Response(
                {"detail": "One or both organizations not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        link = OrganizationLink.objects.create(
            main_organization=main_org,
            link_organization=link_org,
            link_organization_request=OrganizationLink.STATUS_PENDING,
            main_organization_request=OrganizationLink.STATUS_PENDING,
            request_status=False,
        )

        serializer = self.get_serializer(link)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        """Accept link request — either main or link organization can do this."""
        link = self.get_object()
        user = request.user
        user_orgs = user.organizations.all()

        if link.main_organization in user_orgs:
            link.main_organization_request = OrganizationLink.STATUS_ACCEPTED
        elif link.link_organization in user_orgs:
            link.link_organization_request = OrganizationLink.STATUS_ACCEPTED
        else:
            return Response(
                {"detail": "You are not a member of either linked organization."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Auto-set request_status = True when both accepted
        if (
            link.main_organization_request == OrganizationLink.STATUS_ACCEPTED
            and link.link_organization_request == OrganizationLink.STATUS_ACCEPTED
        ):
            link.request_status = True
        else:
            link.request_status = False

        link.save()
        return Response(self.get_serializer(link).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Reject link request — any side can reject, making request_status False."""
        link = self.get_object()
        user = request.user
        user_orgs = user.organizations.all()

        if link.main_organization in user_orgs:
            link.main_organization_request = OrganizationLink.STATUS_REJECTED
        elif link.link_organization in user_orgs:
            link.link_organization_request = OrganizationLink.STATUS_REJECTED
        else:
            return Response(
                {"detail": "You are not a member of either linked organization."},
                status=status.HTTP_403_FORBIDDEN,
            )

        link.request_status = False
        link.save()
        return Response(self.get_serializer(link).data, status=status.HTTP_200_OK)


# -------------------------------------------------------------------
# Other APIs (Organization, Branch, Agency)
# -------------------------------------------------------------------

class OrganizationViewSet(viewsets.ModelViewSet):
    """API for managing Organizations"""
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if user_id:
            query_filters &= Q(user=user_id)
        return Organization.objects.filter(query_filters)


class BranchViewSet(viewsets.ModelViewSet):
    """API for managing Branches"""
    serializer_class = BranchSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization_id")
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if organization_id:
            query_filters &= Q(organization_id=organization_id)
        if user_id:
            query_filters &= Q(user=user_id)
        return Branch.objects.filter(query_filters).select_related("organization")


class AgencyViewSet(viewsets.ModelViewSet):
    """API for managing Agencies"""
    serializer_class = AgencySerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization_id")
        branch_id = self.request.query_params.get("branch_id")
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if organization_id:
            query_filters &= Q(branch__organization_id=organization_id)
        if branch_id:
            query_filters &= Q(branch_id=branch_id)
        if user_id:
            query_filters &= Q(user=user_id)
        return Agency.objects.filter(query_filters).select_related("branch").prefetch_related("files")


class AgencyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agency_id = request.query_params.get("agency_id")
        if not agency_id:
            return Response({"success": False, "message": "agency_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = AgencyProfile.objects.get(agency_id=agency_id)
        except AgencyProfile.DoesNotExist:
            return Response({"success": False, "message": "Agency profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AgencyProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        agency_id = data.get("agency") or data.get("agency_id")
        if not agency_id:
            return Response({"success": False, "message": "agency is required."}, status=status.HTTP_400_BAD_REQUEST)
        data["agency"] = agency_id
        user = request.user if request.user.is_authenticated else None
        try:
            profile = AgencyProfile.objects.get(agency_id=agency_id)
            serializer = AgencyProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(updated_by=user)
                return Response({
                    "success": True,
                    "message": "Agency profile updated successfully",
                    "updated_profile": serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AgencyProfile.DoesNotExist:
            serializer = AgencyProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_by=user, updated_by=user)
                return Response({
                    "success": True,
                    "message": "Agency profile created successfully",
                    "updated_profile": serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RuleCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        data = request.data.copy()
        rule_id = data.get("id")
        user = request.user
        # set defaults
        if "is_active" not in data:
            data["is_active"] = True

        if rule_id:
            rule = get_object_or_404(Rule, id=rule_id)
            serializer = RuleSerializer(rule, data=data, partial=True)
            if serializer.is_valid():
                # ensure updated_by stored as id
                serializer.save(updated_by=user.id if user and user.is_authenticated else None)
                return Response({"success": True, "message": "Rule updated successfully", "rule_id": rule.id})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # create new
        serializer = RuleSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(created_by=user.id if user and user.is_authenticated else None,
                                       updated_by=user.id if user and user.is_authenticated else None)
            return Response({"success": True, "message": "Rule created successfully", "rule_id": instance.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RuleListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        rule_type = request.query_params.get("type")
        page = request.query_params.get("page")
        language = request.query_params.get("language")

        qs = Rule.objects.filter(is_active=True)
        if rule_type:
            qs = qs.filter(rule_type=rule_type)
        if language:
            qs = qs.filter(language=language)
        if page:
            # Attempt to use JSON contains lookup. Some DB backends (sqlite in-memory used by tests)
            # raise NotSupportedError only when the queryset is compiled/executed, not when the
            # filter is constructed. So we apply the filter and force a minimal evaluation to
            # trigger any backend errors and catch them to fall back to a string match.
            try:
                qs = qs.filter(pages_to_display__contains=[page])
                # force-evaluate a small slice to trigger SQL compilation
                list(qs[:1])
            except NotSupportedError:
                # fallback to icontains on the JSON string for backends without JSON contains support
                qs = Rule.objects.filter(is_active=True)
                if rule_type:
                    qs = qs.filter(rule_type=rule_type)
                if language:
                    qs = qs.filter(language=language)
                qs = qs.filter(pages_to_display__icontains=page)

        qs = qs.order_by("-updated_at")
        serializer = RuleSerializer(qs, many=True)
        return Response({"rules": serializer.data})


class RuleUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, id=None):
        rule = get_object_or_404(Rule, id=id)
        serializer = RuleSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user.id if request.user and request.user.is_authenticated else None)
            return Response({"success": True, "message": "Rule updated successfully", "rule_id": rule.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RuleDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id=None):
        rule = get_object_or_404(Rule, id=id)
        rule.is_active = False
        rule.updated_by = request.user.id if request.user and request.user.is_authenticated else None
        rule.save()
        return Response({"success": True, "message": "Rule deleted successfully"})


# -------------------------
# Walk-in booking APIs
# -------------------------


class WalkInCreateView(APIView):
    permission_classes = [IsAuthenticated, IsOrgStaff]

    def post(self, request):
        data = request.data.copy()

        # basic required fields
        hotel_id = data.get("hotel_id") or data.get("hotel")
        org_id = data.get("organization_id") or data.get("organization")
        if not hotel_id or not org_id:
            return Response({"detail": "hotel_id and organization_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        # ensure user belongs to organization (explicit ownership check)
        if not _user_belongs_to_org(request.user, org_id):
            return Response({"detail": "You don't have permission to create bookings for this organization."}, status=status.HTTP_403_FORBIDDEN)

        # normalize hotel & org to pk fields expected by serializer
        data["hotel"] = hotel_id
        data["organization"] = org_id
        serializer = WalkInBookingSerializer(data=data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            instance = serializer.save()
            # mark rooms occupied (will raise ValueError if no free bed exists)
            try:
                instance.mark_rooms_occupied()
            except ValueError as e:
                # rollback the transaction and return conflict
                transaction.set_rollback(True)
                return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)
            except Exception:
                # preserve previous behavior for unexpected errors
                pass

            # Create ledger entries for advance payment (if any) using centralized helper
            try:
                from .ledger_utils import find_account, create_entry_with_lines
            except Exception:
                find_account = create_entry_with_lines = None

            try:
                advance = Decimal(str(instance.advance_paid or 0))
            except Exception:
                advance = Decimal("0")

            if create_entry_with_lines and advance > 0:
                # Prefer CASH or BANK for received money
                cash_acc = find_account(instance.organization_id, ["CASH", "BANK"]) or find_account(None, ["CASH"]) 
                # Use SUSPENSE account to record advance as liability
                suspense_acc = find_account(instance.organization_id, ["SUSPENSE"]) or find_account(None, ["SUSPENSE"]) 

                if cash_acc and suspense_acc:
                    audit_note = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Advance recorded for booking {instance.booking_no} by user {request.user.id if request.user and request.user.is_authenticated else 'unknown'}"
                    create_entry_with_lines(
                        booking_no=instance.booking_no,
                        service_type="hotel",
                        narration=f"Advance payment for walk-in booking {instance.booking_no}",
                        metadata={"booking_id": instance.id, "hotel_id": instance.hotel_id},
                        internal_notes=[audit_note],
                        created_by=request.user if request.user and request.user.is_authenticated else None,
                        lines=[
                            {"account": cash_acc, "debit": advance, "credit": Decimal("0.00")},
                            {"account": suspense_acc, "debit": Decimal("0.00"), "credit": advance},
                        ],
                    )

        return Response({"success": True, "booking_no": instance.booking_no, "booking_id": instance.id}, status=status.HTTP_201_CREATED)


class WalkInListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        status_q = request.query_params.get("status")
        date = request.query_params.get("date")
        hotel_id = request.query_params.get("hotel_id")
        org_id = request.query_params.get("organization_id")

        qs = WalkInBooking.objects.all()
        if status_q:
            qs = qs.filter(status=status_q)
        if hotel_id:
            qs = qs.filter(hotel_id=hotel_id)
        if org_id:
            qs = qs.filter(organization_id=org_id)
        if date:
            # filter bookings with check_in or check_out matching the date in any room_details
            qs = qs.filter(room_details__icontains=date)

        serializer = WalkInBookingSerializer(qs, many=True)
        return Response({"bookings": serializer.data, "total_walkin_bookings": qs.count()})


class WalkInUpdateStatusView(APIView):
    permission_classes = [IsAuthenticated, IsOrgStaff]

    def put(self, request, booking_id=None):
        instance = get_object_or_404(WalkInBooking, id=booking_id)

        # permission: user must belong to organization or be superuser
        if not _user_belongs_to_org(request.user, instance.organization_id):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        status_val = request.data.get("status")
        if not status_val:
            return Response({"detail": "status is required"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # handle transitions
            if status_val == WalkInBooking.STATUS_CHECKED_OUT:
                final_amount = request.data.get("final_amount")
                if final_amount is None:
                    return Response({"detail": "final_amount required for checkout"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    final_amount_dec = Decimal(str(final_amount))
                except Exception:
                    return Response({"detail": "invalid final_amount"}, status=status.HTTP_400_BAD_REQUEST)

                instance.total_amount = final_amount_dec
                instance.status = WalkInBooking.STATUS_CHECKED_OUT
                instance.updated_by = request.user.id if request.user.is_authenticated else None
                instance.save()
                try:
                    instance.mark_rooms_cleaning_pending()
                except Exception:
                    pass
                # Ledger: recognize remaining revenue (final_amount - advance_paid)
                try:
                    advance = Decimal(str(instance.advance_paid or 0))
                except Exception:
                    advance = Decimal("0")

                remaining = final_amount_dec - advance
                # Lazy import ledger models to avoid circular import problems during app registry
                try:
                    from ledger.models import LedgerEntry, LedgerLine, Account
                    from datetime import datetime as _dt
                except Exception:
                    LedgerEntry = LedgerLine = Account = None
                    _dt = None

                if LedgerEntry:
                    # amount recognized from advance (move from SUSPENSE -> SALES)
                    amount_from_advance = min(advance, final_amount_dec)
                    # remaining to be collected at checkout (cash)
                    remaining = final_amount_dec - amount_from_advance

                    # Lazy import again (we're inside function)
                    try:
                        from ledger.models import LedgerEntry, LedgerLine, Account
                        from datetime import datetime as _dt
                    except Exception:
                        LedgerEntry = LedgerLine = Account = None
                        _dt = None

                    if amount_from_advance > 0:
                        try:
                            from .ledger_utils import find_account, create_entry_with_lines
                        except Exception:
                            find_account = create_entry_with_lines = None

                        if create_entry_with_lines:
                            suspense_acc = find_account(instance.organization_id, ["SUSPENSE"]) or find_account(None, ["SUSPENSE"]) 
                            sales_acc = find_account(instance.organization_id, ["SALES"]) or find_account(None, ["SALES"]) 

                            if suspense_acc and sales_acc:
                                audit_note = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Recognize revenue from advance for booking {instance.booking_no} by user {request.user.id if request.user and request.user.is_authenticated else 'unknown'}"
                                create_entry_with_lines(
                                    booking_no=instance.booking_no,
                                    service_type="hotel",
                                    narration=f"Recognize revenue from advance for booking {instance.booking_no}",
                                    metadata={"booking_id": instance.id, "hotel_id": instance.hotel_id},
                                    internal_notes=[audit_note],
                                    created_by=request.user if request.user and request.user.is_authenticated else None,
                                    lines=[
                                        {"account": suspense_acc, "debit": amount_from_advance, "credit": Decimal("0.00")},
                                        {"account": sales_acc, "debit": Decimal("0.00"), "credit": amount_from_advance},
                                    ],
                                )

                    # If there's remaining amount (customer paid at checkout), record cash->sales
                    if remaining > 0:
                        try:
                            from .ledger_utils import find_account, create_entry_with_lines
                        except Exception:
                            find_account = create_entry_with_lines = None

                        if create_entry_with_lines:
                            cash_acc = find_account(instance.organization_id, ["CASH", "BANK"]) or find_account(None, ["CASH"]) 
                            sales_acc = find_account(instance.organization_id, ["SALES"]) or find_account(None, ["SALES"]) 

                            if cash_acc and sales_acc:
                                audit_note = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checkout payment recorded for booking {instance.booking_no} by user {request.user.id if request.user and request.user.is_authenticated else 'unknown'}"
                                create_entry_with_lines(
                                    booking_no=instance.booking_no,
                                    service_type="hotel",
                                    narration=f"Checkout payment for walk-in booking {instance.booking_no}",
                                    metadata={"booking_id": instance.id, "hotel_id": instance.hotel_id},
                                    internal_notes=[audit_note],
                                    created_by=request.user if request.user and request.user.is_authenticated else None,
                                    lines=[
                                        {"account": cash_acc, "debit": remaining, "credit": Decimal("0.00")},
                                        {"account": sales_acc, "debit": Decimal("0.00"), "credit": remaining},
                                    ],
                                )
                    # No additional global checkout entry here — remaining amount is already
                    # recorded above (cash->sales) when applicable. Avoid duplicating entries.

            elif status_val == WalkInBooking.STATUS_AVAILABLE:
                instance.status = WalkInBooking.STATUS_AVAILABLE
                instance.updated_by = request.user.id if request.user.is_authenticated else None
                instance.save()
                try:
                    instance.mark_rooms_available()
                except Exception:
                    pass

            else:
                # other statuses (e.g., checked_in, cleaning_pending)
                if status_val not in dict(WalkInBooking.STATUS_CHOICES):
                    return Response({"detail": "invalid status"}, status=status.HTTP_400_BAD_REQUEST)
                instance.status = status_val
                instance.updated_by = request.user.id if request.user.is_authenticated else None
                instance.save()

        return Response({"success": True, "message": "Status updated", "status": instance.status})


class WalkInSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsOrgStaff]

    def get(self, request):
        hotel_id = request.query_params.get("hotel_id")
        date = request.query_params.get("date")
        if not hotel_id or not date:
            return Response({"detail": "hotel_id and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        total_rooms = HotelRooms.objects.filter(hotel_id=hotel_id).count()
        occupied_rooms = WalkInBooking.objects.filter(hotel_id=hotel_id, status=WalkInBooking.STATUS_CHECKED_IN).count()
        cleaning_pending = WalkInBooking.objects.filter(hotel_id=hotel_id, status=WalkInBooking.STATUS_CLEANING_PENDING).count()
        available_rooms = max(0, total_rooms - occupied_rooms - cleaning_pending)

        # total sales: sum of total_amount for checked_out bookings on that date (simple filter)
        total_sales = WalkInBooking.objects.filter(hotel_id=hotel_id, status=WalkInBooking.STATUS_CHECKED_OUT, updated_at__date=date).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_expense = 0
        profit = total_sales - total_expense

        return Response({
            "hotel_id": int(hotel_id),
            "date": date,
            "total_rooms": total_rooms,
            "occupied_rooms": occupied_rooms,
            "available_rooms": available_rooms,
            "total_sales": total_sales,
            "total_expense": total_expense,
            "profit": profit,
        })

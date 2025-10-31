from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import SimpleRateThrottle
from universal.models import PaxMovement
from django.db.models import Prefetch, Sum, F, Value, DecimalField, FloatField, Count
from django.db.models.functions import Coalesce, Round, Cast
from django.utils.dateparse import parse_datetime, parse_date
from rest_framework.decorators import action
from django.db import connection
from django.db import transaction
from rest_framework import generics
from .serializers import PublicBookingCreateSerializer, PublicPaymentCreateSerializer
from packages.models import UmrahPackage
from leads.models import Lead, FollowUp
from django.contrib.auth import get_user_model
from .models import Booking, Payment
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from organization.models import Agency

# Admin endpoint to approve public payments
class AdminApprovePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, payment_id=None):
        try:
            payment = Payment.objects.select_for_update().get(pk=payment_id)
        except Payment.DoesNotExist:
            return Response({"success": False, "message": "Payment not found"}, status=404)

        if payment.status == 'Completed':
            return Response({"success": True, "message": "Already approved"})

        with transaction.atomic():
            # mark payment completed
            payment.status = 'Completed'
            payment.save(update_fields=['status'])

            # update booking totals
            booking = payment.booking
            # use Decimal for safe arithmetic when model uses DecimalField
            from decimal import Decimal
            try:
                prev = Decimal(str(booking.total_payment_received or 0))
            except Exception:
                prev = Decimal('0')
            try:
                amt = Decimal(str(payment.amount or 0))
            except Exception:
                amt = Decimal('0')

            booking.total_payment_received = prev + amt

            # recompute flags
            try:
                paid = float(booking.total_payment_received or 0)
                total = float(booking.total_amount or 0)
                booking.paid_payment = paid
                booking.pending_payment = max(0.0, total - paid)
                if paid >= total and total > 0:
                    booking.is_paid = True
                    booking.status = 'confirmed'
                booking.save(update_fields=['total_payment_received', 'paid_payment', 'pending_payment', 'is_paid', 'status'])
            except Exception:
                booking.save()

            # ledger entry: record cash received
            try:
                from organization.ledger_utils import find_account, create_entry_with_lines
            except Exception:
                find_account = create_entry_with_lines = None

            if create_entry_with_lines:
                # prefer CASH/BANK for debit and SUSPENSE/RECEIVABLE for credit
                cash_acc = find_account(booking.organization_id, ['CASH', 'BANK']) or find_account(None, ['CASH', 'BANK'])
                suspense_acc = find_account(booking.organization_id, ['SUSPENSE', 'RECEIVABLE']) or find_account(None, ['SUSPENSE', 'RECEIVABLE'])
                if cash_acc and suspense_acc:
                    amount = payment.amount or 0
                    audit_note = f"[auto] Public payment #{payment.id} approved for booking {booking.booking_number}"
                    create_entry_with_lines(
                        booking_no=booking.booking_number,
                        service_type='payment',
                        narration=f"Public payment received for booking {booking.booking_number}",
                        metadata={'payment_id': payment.id, 'booking_id': booking.id},
                        internal_notes=[audit_note],
                        created_by=request.user if request.user.is_authenticated else None,
                        lines=[
                            {'account': cash_acc, 'debit': amount, 'credit': 0},
                            {'account': suspense_acc, 'debit': 0, 'credit': amount},
                        ],
                    )

            # Update follow-ups for this booking: adjust remaining_amount or close if fully paid
            try:
                # recompute remaining after payment
                remaining = float(booking.total_amount or 0) - float(booking.total_payment_received or 0)
            except Exception:
                remaining = None

            if remaining is not None:
                open_fus = FollowUp.objects.filter(booking=booking, status__in=['open', 'pending']).order_by('created_at')
                if remaining <= 0:
                    # close all open follow-ups
                    for fu in open_fus:
                        try:
                            fu.remaining_amount = 0
                            fu.close(user=request.user)
                        except Exception:
                            # best-effort; continue
                            fu.remaining_amount = 0
                            fu.status = 'closed'
                            fu.closed_at = __import__('datetime').datetime.now()
                            fu.save()
                else:
                    # update first open follow-up remaining_amount
                    fu = open_fus.first()
                    if fu:
                        fu.remaining_amount = remaining
                        fu.save()

        return Response({"success": True, "payment_id": payment.id, "status": payment.status})

from .models import (
    Booking,
    BookingHotelDetails,
    BookingTransportDetails,
    BookingTicketDetails,
    BookingTicketTicketTripDetails,
    BookingTicketStopoverDetails,
    BookingPersonDetail,
    Payment,
    Sector,
    BigSector,
    VehicleType,
    InternalNote,
    BankAccount,
    OrganizationLink,
    AllowedReseller,
    DiscountGroup,
    Markup,
    BookingCallRemark
)
from .serializers import BookingSerializer, PaymentSerializer, SectorSerializer, BigSectorSerializer, VehicleTypeSerializer, InternalNoteSerializer, DiscountGroupSerializer, BankAccountSerializer, OrganizationLinkSerializer, AllowedResellerSerializer, MarkupSerializer, BookingCallRemarkSerializer, PublicBookingSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from universal.scope import apply_user_scope

import json
class BookingViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=["get"], url_path="unpaid/(?P<organization_id>[^/.]+)")
    def get_unpaid_orders(self, request, organization_id=None):
        from django.utils import timezone
        now = timezone.now()
        unpaid_bookings = (
            Booking.objects.filter(
                organization_id=organization_id,
                status="unpaid",
                expiry_time__gte=now
            )
            .annotate(
                paid_payment_sum=Coalesce(
                    Sum("payment_details__amount", output_field=FloatField()),
                    Value(0.0, output_field=FloatField())
                ),
                pending_payment_sum=F("total_amount") - Coalesce(
                    Sum("payment_details__amount", output_field=FloatField()),
                    Value(0.0, output_field=FloatField())
                )
            )
            .filter(pending_payment_sum__gt=0)
        )

        results = []
        for booking in unpaid_bookings:
            person = booking.person_details.first()
            results.append({
                "booking_id": booking.id,
                "booking_no": booking.booking_number,
                "customer_name": f"{person.first_name} {person.last_name}".strip() if person else "",
                "contact_number": getattr(person, "contact_number", "") if person else "",
                "total_amount": booking.total_amount,
                "paid_payment": booking.paid_payment_sum,
                "pending_payment": booking.pending_payment_sum,
                "expiry_time": booking.expiry_time,
                "agent_id": getattr(booking, "user_id", None),
                "status": booking.status,
                "call_status": getattr(booking, "call_status", False),
                "client_note": getattr(booking, "client_note", None),
            })

        return Response({
            "total_unpaid": len(results),
            "unpaid_bookings": results
        })
    
    @action(detail=False, methods=["post"], url_path="unpaid/remarks")
    def add_call_remarks(self, request):
        data = request.data
        booking_id = data.get("booking_id")
        call_status = data.get("call_status")
        remarks = data.get("remarks", [])
        created_by = data.get("created_by")

        # Validate booking
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"success": False, "message": "Invalid booking_id."}, status=status.HTTP_400_BAD_REQUEST)

        # Update call_status
        if call_status is not None:
            booking.call_status = call_status
            booking.save(update_fields=["call_status"])

        # Add remarks (support both IDs and new text remarks)
        remarks_created = 0
        for remark in remarks:
            if isinstance(remark, int):
                # If remark is an ID, skip (or you can fetch and link if you have a separate remarks table)
                continue
            if isinstance(remark, str) and remark.strip():
                BookingCallRemark.objects.create(
                    booking=booking,
                    created_by_id=created_by,
                    remark_text=remark.strip(),
                )
                remarks_created += 1

        return Response({
            "success": True,
            "message": "Call remarks added successfully.",
            "data": {
                "booking_id": booking.id,
                "call_status": booking.call_status,
                "remarks_count": remarks_created
            }
        }, status=status.HTTP_200_OK)
    serializer_class = BookingSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    NESTED_FIELDS = [
        "ticket_details",
        "person_details",
        "hotel_details",
        "transport_details",
    ]
    def get_queryset(self):
        """
        Optimized queryset to prevent N+1 queries using select_related and prefetch_related.
        """
        qs = (
            Booking.objects.annotate(
                paid_amount=Coalesce(
                    Sum("payment_details__amount", output_field=FloatField()),
                    Value(0.0, output_field=FloatField()),
                    output_field=FloatField(),
                ),
                remaining_amount=Cast(
                    Round(
                        Cast(F("total_amount"), FloatField()) - Coalesce(
                            Sum("payment_details__amount", output_field=FloatField()),
                            Value(0.0, output_field=FloatField()),
                            output_field=FloatField(),
                        ),
                        2  # round to 2 decimals
                    ),
                    FloatField()
                )
            )
            .prefetch_related(
                "hotel_details",
                "transport_details",
                Prefetch(
                    "ticket_details",
                    queryset=BookingTicketDetails.objects.prefetch_related(
                        "trip_details", "stopover_details"
                    ),
                ),
                "person_details",
                "payment_details",
            )
            .order_by("-date")
        )
        booking_number = self.request.query_params.get("booking_number")
        if booking_number:
            qs = qs.filter(booking_number=booking_number)
    
        return qs


class PublicBookingCreateAPIView(generics.CreateAPIView):
    """Create a public booking for an Umrah package.

    Expected payload (JSON):
      - umrah_package_id, total_pax, contact_name, contact_phone
      - optional: total_adult/child/infant, contact_email, pay_now, pay_amount

    Creates Booking (is_public_booking=True), decreases package left_seats, creates a Lead,
    and optionally creates a Payment (public_mode=True, status='Pending').
    """
    permission_classes = [AllowAny]
    serializer_class = PublicBookingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        pkg = UmrahPackage.objects.select_for_update().get(pk=data['umrah_package_id'])

        User = get_user_model()
        system_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

        with transaction.atomic():
            # double-check seats under lock
            pkg.refresh_from_db()
            total_pax = int(data['total_pax'])
            if (pkg.left_seats or 0) < total_pax:
                return Response({"success": False, "message": f"Only {pkg.left_seats or 0} seats left"}, status=400)

            # create booking_number
            import secrets, time
            booking_number = f"PB-{int(time.time())}-{secrets.token_hex(3).upper()}"

            org = pkg.organization
            # choose first branch if available
            branch = None
            try:
                branch = org.branches.first()
            except Exception:
                branch = None

            # choose or create an agency to satisfy non-null FK
            agency = None
            try:
                if branch:
                    agency = branch.agencies.first()
                if not agency:
                    agency = org.agencies.first()
                if not agency and branch:
                    # create a lightweight Agency record for public bookings
                    agency = Agency.objects.create(branch=branch, name='Public Agency')
            except Exception:
                agency = None

            booking = Booking.objects.create(
                user=system_user,
                organization=org,
                branch=branch,
                agency=agency,
                booking_number=booking_number,
                total_pax=total_pax,
                total_adult=data.get('total_adult', 0) or 0,
                total_child=data.get('total_child', 0) or 0,
                total_infant=data.get('total_infant', 0) or 0,
                total_amount=float((pkg.price_per_person or 0) * total_pax),
                status='unpaid',
                payment_status='Pending',
                is_public_booking=True,
                created_by_user_type='customer',
                umrah_package=pkg,
            )

            # generate invoice_no and save
            try:
                booking.generate_invoice_no()
                booking.save(update_fields=['invoice_no'])
            except Exception:
                pass

            # decrement package seats
            try:
                pkg.booked_seats = (pkg.booked_seats or 0) + total_pax
                pkg.left_seats = max(0, (pkg.left_seats or 0) - total_pax)
                pkg.save(update_fields=['booked_seats', 'left_seats'])
            except Exception:
                pass

            # create a lead
            lead = None
            try:
                lead = Lead.objects.create(
                    customer_full_name=data.get('contact_name'),
                    contact_number=data.get('contact_phone'),
                    email=data.get('contact_email'),
                    branch=branch,
                    organization=org,
                    lead_source='whatsapp',
                    lead_status='new',
                    interested_in='umrah',
                    booking=booking,
                )
            except Exception:
                # don't fail booking creation if lead creation fails
                lead = None

            payment = None
            if data.get('pay_now'):
                amount = float(data.get('pay_amount') or booking.total_amount)
                payment = Payment.objects.create(
                    organization=org,
                    branch=branch,
                    booking=booking,
                    method='online',
                    amount=amount,
                    status='Pending',
                    public_mode=True,
                )

            # create follow-up if partial payment
            try:
                paid = float(payment.amount) if payment else 0.0
                remaining = float(booking.total_amount or 0) - paid
                if remaining > 0:
                    from leads.models import FollowUp as LF
                    fu = LF.objects.create(
                        booking=booking,
                        lead=lead,
                        remaining_amount=remaining,
                        status='open',
                        notes='Auto follow-up for remaining payment on public booking',
                        created_by=system_user,
                    )
                    # notify sales/admin asynchronously after commit (if notification util exists)
                    try:
                        from django.db import transaction as _tx
                        def _notify():
                            try:
                                from notifications import services as _ns
                                _ns.enqueue_followup_created(fu.id)
                            except Exception:
                                pass
                        _tx.on_commit(_notify)
                    except Exception:
                        pass
            except Exception:
                pass

        # Response
        resp = {
            "success": True,
            "booking_number": booking.booking_number,
            "invoice_no": booking.invoice_no,
            "total_amount": float(booking.total_amount or 0),
            "remaining_balance": float(booking.total_amount or 0) - (float(payment.amount) if payment else 0),
            "payment_id": getattr(payment, 'id', None),
        }

        # notify booking created and pending payment created (best-effort) after commit
        try:
            from django.db import transaction as _tx
            def _notify_booking():
                try:
                    from notifications import services as _ns
                    _ns.enqueue_public_booking_created(booking.id)
                    if payment:
                        _ns.enqueue_public_payment_created(payment.id)
                except Exception:
                    pass
            _tx.on_commit(_notify_booking)
        except Exception:
            pass
        return Response(resp, status=201)


class PublicBookingPaymentCreateAPIView(generics.CreateAPIView):
    """Create a public payment for a booking (public_mode=True).

    Admin will later approve/verify these payments via admin endpoints.
    """
    permission_classes = [AllowAny]
    serializer_class = PublicPaymentCreateSerializer

    def create(self, request, booking_number=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            booking = Booking.objects.get(booking_number=data['booking_number'])
        except Booking.DoesNotExist:
            return Response({"success": False, "message": "Invalid booking_number"}, status=400)

        with transaction.atomic():
            org = booking.organization
            branch = booking.branch
            payment = Payment.objects.create(
                organization=org,
                branch=branch,
                booking=booking,
                method=data.get('method', 'online'),
                amount=float(data['amount']),
                status='Pending',
                public_mode=True,
                transaction_number=data.get('transaction_number'),
            )

            # After creating a public payment (pending), create or update a FollowUp
            try:
                User = get_user_model()
                system_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
            except Exception:
                system_user = None

            try:
                paid = float(payment.amount) if payment else 0.0
                remaining = float(booking.total_amount or 0) - paid
                if remaining > 0:
                    # prefer existing open follow-up for booking
                    fu = FollowUp.objects.filter(booking=booking, status__in=['open', 'pending']).order_by('created_at').first()
                    if fu:
                        fu.remaining_amount = remaining
                        fu.save()
                    else:
                        # attach to any lead associated with booking if present
                        lead = None
                        try:
                            lead = booking.lead_set.first()
                        except Exception:
                            lead = None
                        fu = FollowUp.objects.create(
                            booking=booking,
                            lead=lead,
                            remaining_amount=remaining,
                            status='open',
                            notes='Auto follow-up for remaining payment (public payment created)',
                            created_by=system_user,
                        )

                    # enqueue a notification for follow-up creation (best-effort)
                    try:
                        from django.db import transaction as _tx
                        def _notify_fu():
                            try:
                                from notifications import services as _ns
                                _ns.enqueue_followup_created(fu.id)
                            except Exception:
                                pass
                        _tx.on_commit(_notify_fu)
                    except Exception:
                        pass

            except Exception:
                # Best-effort; do not fail payment creation if follow-up logic fails
                pass

        return Response({"success": True, "payment_id": payment.id, "status": payment.status}, status=201)
    @action(detail=False, methods=["get"], url_path="by-ticket")
    def by_ticket(self, request):
        ticket_id = request.query_params.get("ticket_id")
        if not ticket_id:
            return Response({"error": "ticket_id is required"}, status=400)

        query = """
        SELECT 
            tickets_ticket.id AS id, 
            tickets_ticket.is_meal_included as is_meal_included,
            tickets_ticket.is_refundable as is_refundable,
            tickets_ticket.pnr as pnr,
            tickets_ticket.child_price as child_price,
            tickets_ticket.infant_price as infant_price,
            tickets_ticket.adult_price as adult_price,
            tickets_ticket.total_seats as total_seats,
            tickets_ticket.left_seats as left_seats,
            tickets_ticket.booked_tickets as booked_tickets,
            tickets_ticket.confirmed_tickets as confirmed_tickets,
            tickets_ticket.weight as weight,
            tickets_ticket.pieces as pieces,
            tickets_ticket.is_umrah_seat as is_umrah_seat,
            tickets_ticket.trip_type as trip_type,
            tickets_ticket.departure_stay_type as departure_stay_type,
            tickets_ticket.return_stay_type as return_stay_type,
            tickets_ticket.status as status,
            tickets_ticket.organization_id as organization_id,
            tickets_ticket.airline_id as airline_id,
            tickets_tickettripdetails.id as trip_id,
            tickets_tickettripdetails.departure_date_time as departure_date_time,
            tickets_tickettripdetails.arrival_date_time as arrival_date_time,
            tickets_tickettripdetails.trip_type as trip_type,
            tickets_tickettripdetails.departure_city_id as departure_city,
            tickets_tickettripdetails.arrival_city_id as arrival_city,
            booking_bookingticketstopoverdetails.stopover_duration as stopover_duration,
            booking_bookingticketstopoverdetails.trip_type as stop_trip_type,
            booking_bookingticketstopoverdetails.stopover_city_id as stopover_city,
            organization_agency.name as agency_name,
            organization_agency.address as agency_address,
            organization_agency.ageny_name AS agency_name2,
            organization_agency.agreement_status AS agency_agreement_status,
            organization_agency.email AS agency_email,
            organization_agency.phone_number AS agency_phone,
            organization_agency.logo AS agency_logo,
            booking_bookingpersondetail.age_group as person_age_group,
            booking_bookingpersondetail.person_title as person_title,
            booking_bookingpersondetail.first_name as person_first_name,
            booking_bookingpersondetail.last_name as person_last_name,
            booking_bookingpersondetail.passport_number as person_passport_number,
            booking_bookingpersondetail.date_of_birth as person_date_of_birth,
            booking_bookingpersondetail.passpoet_issue_date as person_passpoet_issue_date,
            booking_bookingpersondetail.passport_expiry_date as person_passport_expiry_date,
            booking_bookingpersondetail.country as person_passport_country,
            booking_bookingpersondetail.ticket_price as person_ticket_price,
            booking_booking.total_ticket_amount_pkr as total_ticket_amount_pkr,
            booking_booking.status as booking_status,
            booking_booking.is_paid as booking_is_paid,
            booking_booking.category as booking_category
        FROM tickets_ticket 
        JOIN tickets_tickettripdetails ON tickets_ticket.id=tickets_tickettripdetails.ticket_id 
        JOIN booking_bookingticketdetails ON tickets_ticket.id= booking_bookingticketdetails.ticket_id 
        JOIN booking_booking ON booking_bookingticketdetails.booking_id = booking_booking.id 
        JOIN booking_bookingticketstopoverdetails ON tickets_ticket.id=booking_bookingticketstopoverdetails.ticket_id 
        JOIN organization_agency ON booking_booking.agency_id=organization_agency.id 
        JOIN booking_bookingpersondetail ON booking_booking.id= booking_bookingpersondetail.booking_id
        WHERE tickets_ticket.id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [ticket_id])
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not result:
            return Response({"error": "No booking found for this ticket_id"}, status=404)

        return Response(result)
    # @action(detail=False, methods=["get"], url_path="by-ticket")
    # def by_ticket(self, request):
    #     ticket_id = request.query_params.get("ticket_id")
    #     if not ticket_id:
    #         return Response({"error": "ticket_id is required"}, status=400)
    
    #     booking = (
    #         self.get_queryset()
    #         .filter(ticket_details__id=ticket_id)
    #         .first()
    #     )
    
    #     if not booking:
    #         return Response({"error": "No booking found for this ticket_id"}, status=404)
    
    #     serializer = self.get_serializer(booking)
    #     data = serializer.data
    
    #     # ✅ sirf required fields pick karo
    #     filtered_data = {
    #         "ticket_details": data.get("ticket_details", []),
    #         "agency": data.get("agency", {}),
    #         "user": data.get("user", {}),  # agent details
    #         "order_number": data.get("booking_number"),
    #         "persons": [
    #             {
    #                 "age_group": p.get("age_group"),
    #                 "person_title": p.get("person_title"),
    #                 "first_name": p.get("first_name"),
    #                 "last_name": p.get("last_name"),
    #                 "passport_number": p.get("passport_number"),
    #                 "date_of_birth": p.get("date_of_birth"),
    #                 "passpoet_issue_date": p.get("passpoet_issue_date"),
    #                 "passport_expiry_date": p.get("passport_expiry_date"),
    #                 "country": p.get("country"),
    #                 "ticket_price": p.get("ticket_price"),
    #             }
    #             for p in data.get("person_details", [])
    #         ],
    #         "total_ticket_amount_pkr": data.get("total_ticket_amount_pkr", 0),
    #         "status": data.get("status"),
    #         "is_paid": data.get("is_paid"),
    #         "category": data.get("category"),
    #     }
    
    #     return Response(filtered_data)
    @action(detail=False, methods=["get"])
    def get_by_umrah_package(self, request):
        package_id = request.query_params.get("umrah_package_id")
        if not package_id:
            return Response(
                {"error": "Missing 'umrah_package_id' query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bookings = Booking.objects.filter(umrah_package_id=package_id).select_related(
            "user", "organization", "branch", "agency", "umrah_package"
        )

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)



    def _parse_to_list(self, val):
        """Return a list of dicts from val (str JSON / dict / list) or [] on failure."""
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
            except Exception:
                return []
        elif isinstance(val, dict):
            return [val]
        elif isinstance(val, list):
            parsed = val
        else:
            return []

        if isinstance(parsed, dict):
            return [parsed]
        if isinstance(parsed, list):
            return parsed
        return []

    def _normalize_data(self, request):
        """
        Convert request.data (QueryDict) â†’ plain dict with proper nested Python lists/dicts.
        IMPORTANT: Do NOT return a QueryDict; return a normal dict.
        """
        raw = request.data
        out = {}

        # If it's a QueryDict, use get() for first item; else treat it like a normal dict
        is_qd = hasattr(raw, "getlist")

        for key in (raw.keys() if is_qd else raw):
            value = raw.get(key) if is_qd else raw.get(key)

            if key in self.NESTED_FIELDS:
                out[key] = self._parse_to_list(value)
            else:
                out[key] = value  # let serializer coerce scalars (ints/bools/dates)

        # Attach uploaded passport picture to the right person record
        persons = out.get("person_details")
        if isinstance(persons, list):
            for person in persons:
                if isinstance(person, dict) and "passport_picture_field" in person:
                    ref = person["passport_picture_field"]
                    file_key = f"person_files[{ref}]"
                    file_obj = request.FILES.get(file_key)
                    if file_obj:
                        person["passport_picture"] = file_obj

        return out


class AdminPublicBookingViewSet(viewsets.ModelViewSet):
    """Admin endpoints for public bookings: list, retrieve and actions: confirm, cancel, verify_payment."""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PublicBookingSerializer

    def get_queryset(self):
        qs = Booking.objects.filter(is_public_booking=True).prefetch_related('person_details', 'payment_details').order_by('-date')
        # allow optional filtering by status/booking_number
        booking_no = self.request.query_params.get('booking_number')
        status_q = self.request.query_params.get('status')
        if booking_no:
            qs = qs.filter(booking_number=booking_no)
        if status_q:
            qs = qs.filter(status=status_q)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        results = []
        for b in qs:
            person = b.person_details.first()
            lead_id = None
            try:
                lead = b.lead_set.first()
                lead_id = lead.id if lead else None
            except Exception:
                lead_id = None

            # payment status summary
            paid = float(b.total_payment_received or 0)
            total = float(b.total_amount or 0)
            payment_status = 'paid' if paid >= total and total > 0 else ('partial' if paid > 0 else 'unpaid')

            # customers list sorted by paid/unpaid (person-level paid info may not exist; group-level fallback)
            persons = []
            for p in b.person_details.all():
                persons.append({
                    'id': p.id,
                    'first_name': p.first_name,
                    'last_name': p.last_name,
                    'contact_number': getattr(p, 'contact_number', None),
                    'passport_number': getattr(p, 'passport_number', None),
                    'ticket_price': float(p.ticket_price or 0),
                    'is_paid': None,  # per-person payment mapping not tracked here
                })

            # sort persons by ticket_price desc (proxy for paid/unpaid grouping) — leave paid flag null
            persons = sorted(persons, key=lambda x: x.get('ticket_price', 0), reverse=True)

            results.append({
                'id': b.id,
                'booking_number': b.booking_number,
                'invoice_no': b.invoice_no,
                'customer_name': f"{person.first_name if person else ''} {person.last_name if person else ''}".strip(),
                'contact_number': getattr(person, 'contact_number', '') if person else '',
                'payment_status': payment_status,
                'lead_id': lead_id,
                'total_amount': total,
                'paid_amount': paid,
                'pending_amount': max(0.0, total - paid),
                'persons': persons,
                'status': b.status,
                'created_at': b.created_at,
            })

        return Response({'count': len(results), 'results': results})

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm_booking(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk, is_public_booking=True)
        except Booking.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

        booking.status = 'confirmed'
        booking.save(update_fields=['status'])

        # try to notify customer/sales via on_commit hook (best-effort)
        try:
            def _notify():
                try:
                    from notifications import services as _ns
                    _ns.enqueue_booking_confirmed(booking.id)
                except Exception:
                    pass
            transaction.on_commit(_notify)
        except Exception:
            pass

        # update package confirmed seats if applicable
        try:
            pkg = getattr(booking, 'umrah_package', None)
            if pkg:
                pkg.confirmed_seats = (pkg.confirmed_seats or 0) + (booking.total_pax or 0)
                pkg.save(update_fields=['confirmed_seats'])
        except Exception:
            pass

        return Response({'success': True, 'booking_id': booking.id, 'status': booking.status})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_booking(self, request, pk=None):
        try:
            booking = Booking.objects.select_related('umrah_package').get(pk=pk, is_public_booking=True)
        except Booking.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)
        # capture previous status to adjust confirmed seats if needed
        prev_status = getattr(booking, 'status', None)

        # mark canceled and free up package seats if associated
        booking.status = 'canceled'
        booking.save(update_fields=['status'])

        try:
            pkg = booking.umrah_package
            if pkg:
                # free seats
                pkg.left_seats = (pkg.left_seats or 0) + (booking.total_pax or 0)
                pkg.booked_seats = max(0, (pkg.booked_seats or 0) - (booking.total_pax or 0))
                # if booking was previously confirmed, reduce confirmed_seats
                if str(prev_status).lower() == 'confirmed':
                    pkg.confirmed_seats = max(0, (pkg.confirmed_seats or 0) - (booking.total_pax or 0))
                pkg.save(update_fields=['left_seats', 'booked_seats', 'confirmed_seats'])
        except Exception:
            pass

        # notify cancellation
        try:
            def _notify_cancel():
                try:
                    from notifications import services as _ns
                    _ns.enqueue_booking_canceled(booking.id)
                except Exception:
                    pass
            transaction.on_commit(_notify_cancel)
        except Exception:
            pass

        return Response({'success': True, 'booking_id': booking.id, 'status': booking.status})

    @action(detail=True, methods=['post'], url_path='verify-payment')
    def verify_payment(self, request, pk=None):
        """Approve a public payment associated with this booking.
        Accepts POST body: {"payment_id": <id>} or will attempt to approve the latest pending public payment.
        """
        payment_id = request.data.get('payment_id')
        try:
            booking = Booking.objects.get(pk=pk, is_public_booking=True)
        except Booking.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

        payment = None
        if payment_id:
            payment = Payment.objects.filter(pk=payment_id, booking=booking, public_mode=True).first()
        if not payment:
            payment = Payment.objects.filter(booking=booking, public_mode=True, status='Pending').order_by('-id').first()
        if not payment:
            return Response({'detail': 'No pending payment found'}, status=404)

        # reuse admin approval logic (similar to AdminApprovePaymentAPIView)
        from decimal import Decimal
        with transaction.atomic():
            payment.status = 'Completed'
            payment.save(update_fields=['status'])

            try:
                prev = Decimal(str(booking.total_payment_received or 0))
            except Exception:
                prev = Decimal('0')
            try:
                amt = Decimal(str(payment.amount or 0))
            except Exception:
                amt = Decimal('0')

            booking.total_payment_received = prev + amt
            try:
                paid = float(booking.total_payment_received or 0)
                total = float(booking.total_amount or 0)
                booking.paid_payment = paid
                booking.pending_payment = max(0.0, total - paid)
                if paid >= total and total > 0:
                    booking.is_paid = True
                    booking.status = 'confirmed'
                booking.save(update_fields=['total_payment_received', 'paid_payment', 'pending_payment', 'is_paid', 'status'])
            except Exception:
                booking.save()

            # ledger entry (best-effort)
            try:
                from organization.ledger_utils import find_account, create_entry_with_lines
            except Exception:
                find_account = create_entry_with_lines = None

            if create_entry_with_lines:
                cash_acc = find_account(booking.organization_id, ['CASH', 'BANK']) or find_account(None, ['CASH', 'BANK'])
                suspense_acc = find_account(booking.organization_id, ['SUSPENSE', 'RECEIVABLE']) or find_account(None, ['SUSPENSE', 'RECEIVABLE'])
                if cash_acc and suspense_acc:
                    amount = payment.amount or 0
                    audit_note = f"[auto] Public payment #{payment.id} approved for booking {booking.booking_number}"
                    create_entry_with_lines(
                        booking_no=booking.booking_number,
                        service_type='payment',
                        narration=f"Public payment received for booking {booking.booking_number}",
                        metadata={'payment_id': payment.id, 'booking_id': booking.id},
                        internal_notes=[audit_note],
                        created_by=request.user if request.user.is_authenticated else None,
                        lines=[
                            {'account': cash_acc, 'debit': amount, 'credit': 0},
                            {'account': suspense_acc, 'debit': 0, 'credit': amount},
                        ],
                    )

            # update follow-ups similar to AdminApprovePaymentAPIView
            try:
                remaining = float(booking.total_amount or 0) - float(booking.total_payment_received or 0)
            except Exception:
                remaining = None

            if remaining is not None:
                open_fus = FollowUp.objects.filter(booking=booking, status__in=['open', 'pending']).order_by('created_at')
                if remaining <= 0:
                    for fu in open_fus:
                        try:
                            fu.remaining_amount = 0
                            fu.close(user=request.user)
                        except Exception:
                            fu.remaining_amount = 0
                            fu.status = 'closed'
                            fu.closed_at = __import__('datetime').datetime.now()
                            fu.save()
                else:
                    fu = open_fus.first()
                    if fu:
                        fu.remaining_amount = remaining
                        fu.save()

        return Response({'success': True, 'payment_id': payment.id, 'booking_id': booking.id})


class PublicBookingRateThrottle(SimpleRateThrottle):
    """Simple per-IP throttle for public booking endpoint."""
    scope = "public_booking"

    def get_rate(self):
        # Fixed rate for now. Can be moved to settings if desired.
        return "10/min"

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class PublicBookingStatusAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [PublicBookingRateThrottle]

    def get(self, request, booking_no=None):
        ref = request.query_params.get("ref")

        # validate booking_no when present to avoid path traversal / abusive lookup
        if booking_no:
            import re
            # allow alphanumerics, dash, underscore; reasonable max length
            if not re.match(r'^[A-Za-z0-9\-\_]{1,60}$', booking_no):
                return Response({"detail": "Invalid booking number format."}, status=status.HTTP_400_BAD_REQUEST)

        # support three modes: /.../<booking_no>/?ref=..., /...?ref=..., /.../<booking_no>/
        booking = None
        if ref and not booking_no:
            booking = Booking.objects.filter(public_ref=ref).first()
        elif booking_no and ref:
            booking = Booking.objects.filter(booking_number=booking_no, public_ref=ref).first()
        elif booking_no:
            booking = Booking.objects.filter(booking_number=booking_no).first()
        else:
            # ref-only via query param
            if ref:
                booking = Booking.objects.filter(public_ref=ref).first()

        if not booking:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # check expiry
        from django.utils import timezone
        if booking.expiry_time and booking.expiry_time < timezone.now():
            return Response({"detail": "Booking expired."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PublicBookingSerializer(booking, context={"request": request})
        return Response(serializer.data)
    
    # The public booking view is read-only for status lookups. Create/update
    # behavior is handled by the internal BookingViewSet. Keep this APIView
    # focused on GET lookups to avoid exposing write actions publicly.


class PaxSummaryAPIView(APIView):
    """Simple Pax summary aggregator.

    Query params:
      - date_from, date_to (ISO date)
      - group_by (booking_type|status) — default booking_type

    Response: { total_bookings, total_pax, breakdown: [{key, bookings, pax}] }
    """
    permission_classes = []  # use default auth elsewhere; rely on apply_user_scope

    def get(self, request):
        qs = Booking.objects.all()

        # apply user scope so callers only see their allowed data
        qs = apply_user_scope(qs, request.user)

        # date filtering (created_at is used for booking creation time when available)
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        if date_from:
            # accept date or datetime
            dt = parse_date(date_from) or parse_datetime(date_from)
            if dt:
                qs = qs.filter(created_at__gte=dt)
        if date_to:
            dt = parse_date(date_to) or parse_datetime(date_to)
            if dt:
                # include the whole day if date provided
                if isinstance(dt, (type(None),)):
                    qs = qs.filter(created_at__lte=dt)
                else:
                    qs = qs.filter(created_at__lte=dt)

        group_by = request.query_params.get("group_by", "booking_type")

        # map group_by to model field
        if group_by == "status":
            key_field = "status"
        elif group_by == "organization":
            key_field = "organization_id"
        elif group_by == "branch":
            key_field = "branch_id"
        elif group_by == "agency":
            key_field = "agency_id"
        else:
            key_field = "booking_type"

        # use DB aggregation: Count bookings and Sum total_pax
        agg_qs = (
            qs.values(key_field)
            .annotate(bookings=Count("id"), pax=Coalesce(Sum("total_pax", output_field=FloatField()), Value(0, output_field=FloatField()), output_field=FloatField()))
            .order_by()
        )

        breakdown = []
        for row in agg_qs:
            key = row.get(key_field)
            # For foreign keys, present the id (caller can resolve names separately if needed)
            breakdown.append({"key": key, "bookings": int(row.get("bookings") or 0), "pax": float(row.get("pax") or 0)})

        total_bookings = sum(item["bookings"] for item in breakdown)
        total_pax = sum(item["pax"] for item in breakdown)

        return Response({"total_bookings": total_bookings, "total_pax": total_pax, "breakdown": breakdown})
    


class HotelPaxSummaryAPIView(APIView):
    """Return aggregated bookings/pax per hotel."""
    permission_classes = []

    def get(self, request):
        # base booking queryset with scope and date filters
        bs = Booking.objects.all()
        bs = apply_user_scope(bs, request.user)

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        if date_from:
            dt = parse_date(date_from) or parse_datetime(date_from)
            if dt:
                bs = bs.filter(created_at__gte=dt)
        if date_to:
            dt = parse_date(date_to) or parse_datetime(date_to)
            if dt:
                bs = bs.filter(created_at__lte=dt)

        # aggregate over BookingHotelDetails to avoid duplicated bookings
        agg_qs = (
            BookingHotelDetails.objects.filter(booking__in=bs)
            .values("hotel__name", "hotel__city__name")
            .annotate(bookings=Count("booking", distinct=True), pax=Coalesce(Sum("booking__total_pax", output_field=FloatField()), Value(0, output_field=FloatField()), output_field=FloatField()))
            .order_by()
        )

        out = []
        for row in agg_qs:
            out.append({
                "hotel": row.get("hotel__name"),
                "city": row.get("hotel__city__name"),
                "bookings": int(row.get("bookings") or 0),
                "pax": float(row.get("pax") or 0.0),
            })

        return Response(out)


class TransportPaxSummaryAPIView(APIView):
    """Return aggregated bookings/pax per transport vehicle and route."""
    permission_classes = []

    def get(self, request):
        bs = Booking.objects.all()
        bs = apply_user_scope(bs, request.user)

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        if date_from:
            dt = parse_date(date_from) or parse_datetime(date_from)
            if dt:
                bs = bs.filter(created_at__gte=dt)
        if date_to:
            dt = parse_date(date_to) or parse_datetime(date_to)
            if dt:
                bs = bs.filter(created_at__lte=dt)

        # group by vehicle type name and small sector (route)
        agg_qs = (
            BookingTransportDetails.objects.filter(booking__in=bs)
            .values("vehicle_type__vehicle_name", "vehicle_type__small_sector__departure_city__name", "vehicle_type__small_sector__arrival_city__name")
            .annotate(bookings=Count("booking", distinct=True), pax=Coalesce(Sum("booking__total_pax", output_field=FloatField()), Value(0, output_field=FloatField()), output_field=FloatField()))
            .order_by()
        )

        out = []
        for row in agg_qs:
            dep = row.get("vehicle_type__small_sector__departure_city__name")
            arr = row.get("vehicle_type__small_sector__arrival_city__name")
            route = None
            if dep or arr:
                route = f"{dep or '---'} → {arr or '---'}"

            out.append({
                "transport": row.get("vehicle_type__vehicle_name"),
                "route": route,
                "bookings": int(row.get("bookings") or 0),
                "pax": float(row.get("pax") or 0.0),
            })

        return Response(out)


class FlightPaxSummaryAPIView(APIView):
    """Return aggregated bookings/pax per airline and sector (departure → arrival)."""
    permission_classes = []

    def get(self, request):
        bs = Booking.objects.all()
        bs = apply_user_scope(bs, request.user)

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        if date_from:
            dt = parse_date(date_from) or parse_datetime(date_from)
            if dt:
                bs = bs.filter(created_at__gte=dt)
        if date_to:
            dt = parse_date(date_to) or parse_datetime(date_to)
            if dt:
                bs = bs.filter(created_at__lte=dt)

        # aggregate over BookingTicketDetails
        agg_qs = (
            BookingTicketDetails.objects.filter(booking__in=bs)
            .values("ticket__airline__name", "ticket__trip_details__departure_city__name", "ticket__trip_details__arrival_city__name")
            .annotate(bookings=Count("booking", distinct=True), pax=Coalesce(Sum("booking__total_pax", output_field=FloatField()), Value(0, output_field=FloatField()), output_field=FloatField()))
            .order_by()
        )

        out = []
        for row in agg_qs:
            dep = row.get("ticket__trip_details__departure_city__name")
            arr = row.get("ticket__trip_details__arrival_city__name")
            sector = None
            if dep or arr:
                sector = f"{dep or '---'} → {arr or '---'}"

            out.append({
                "airline": row.get("ticket__airline__name"),
                "sector": sector,
                "bookings": int(row.get("bookings") or 0),
                "pax": float(row.get("pax") or 0.0),
            })

        return Response(out)
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    # (Payment-related helpers were moved into PaymentViewSet to avoid
    # accidentally overriding HotelOutsourcingViewSet.get_queryset/create.)

    # (Payment-related helpers were moved into PaymentViewSet to avoid
    # accidentally overriding HotelOutsourcingViewSet.get_queryset/create.)


from rest_framework import permissions
from .serializers import HotelOutsourcingSerializer
from .models import HotelOutsourcing


class HotelOutsourcingViewSet(viewsets.ModelViewSet):
    """API for managing external hotel outsourcing records.

    POST /api/booking/hotel-outsourcing
    GET  /api/booking/hotel-outsourcing
    PATCH /api/booking/hotel-outsourcing/{id}/payment-status -> custom action below
    """
    serializer_class = HotelOutsourcingSerializer
    queryset = HotelOutsourcing.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = HotelOutsourcing.objects.filter(is_deleted=False).order_by('-created_at')
        params = self.request.query_params
        org = params.get('organization_id')
        branch = params.get('branch_id')
        booking_id = params.get('booking_id')
        hotel_name = params.get('hotel_name')
        status = params.get('status')

        if org:
            qs = qs.filter(booking__organization_id=org)
        if branch:
            qs = qs.filter(booking__branch_id=branch)
        if booking_id:
            qs = qs.filter(booking_id=booking_id)
        if hotel_name:
            qs = qs.filter(hotel_name__icontains=hotel_name)
        if status:
            if status.lower() == 'paid':
                qs = qs.filter(is_paid=True)
            elif status.lower() == 'pending':
                qs = qs.filter(is_paid=False)

        # Agents should see only their own bookings (best-effort: non-staff users)
        user = self.request.user
        try:
            if not user.is_staff:
                qs = qs.filter(booking__user_id=user.id)
        except Exception:
            pass

        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        # simple limit/offset pagination
        try:
            limit = int(request.query_params.get('limit', 25))
            offset = int(request.query_params.get('offset', 0))
        except Exception:
            limit = 25
            offset = 0

        total = qs.count()
        objs = qs[offset: offset + limit]
        serializer = self.get_serializer(objs, many=True)
        return Response({
            'count': total,
            'limit': limit,
            'offset': offset,
            'results': serializer.data,
        })

    @action(detail=True, methods=['patch'], url_path='payment-status')
    def payment_status(self, request, pk=None):
        """Toggle/Set payment status for an outsourcing record and update ledger metadata.

        Idempotency: if the linked ledger entry is already marked settled, do not create a
        duplicate settlement entry when marking as paid.
        """
        obj = self.get_object()
        is_paid = request.data.get('is_paid')
        if is_paid is None:
            return Response({'detail': 'is_paid is required'}, status=400)

        from django.db import transaction
        from decimal import Decimal

        with transaction.atomic():
            obj.is_paid = bool(is_paid)
            obj.save()

            # If marking paid, create settlement ledger entry (debit payable, credit cash/bank)
            try:
                from organization.ledger_utils import create_settlement_entry, mark_entry_settled

                if obj.is_paid and obj.ledger_entry_id:
                    amount = Decimal(str(obj.outsource_cost or 0))
                    # Idempotency guard: if the source ledger entry is already marked settled,
                    # skip creating a new settlement entry.
                    try:
                        from ledger.models import LedgerEntry as _LedgerEntry
                        src = _LedgerEntry.objects.filter(pk=obj.ledger_entry_id).first()
                    except Exception:
                        src = None

                    already_settled = False
                    if src:
                        meta = src.metadata or {}
                        already_settled = bool(meta.get('settled'))

                    if not already_settled:
                        # create settlement entry and mark original settled
                        sat = create_settlement_entry(obj.ledger_entry_id, amount, booking=obj.booking, org=obj.booking.organization_id, branch=obj.booking.branch_id, created_by=getattr(request, 'user', None))
                        mark_entry_settled(obj.ledger_entry_id, by_user=getattr(request, 'user', None), settled=True)
                    else:
                        # nothing to do; idempotent
                        sat = None
                    # link settlement entry id if needed
                    if sat:
                        meta = obj.__dict__.get('ledger_entry_id')
                else:
                    # mark original ledger entry as unsettled
                    if obj.ledger_entry_id:
                        mark_entry_settled(obj.ledger_entry_id, by_user=getattr(request, 'user', None), settled=False)
            except Exception:
                # don't fail the endpoint if ledger ops fail; surface minimal response instead
                pass

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    # PaymentViewSet methods intentionally implemented in PaymentViewSet class above.
class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Sector created successfully!", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Sector updated successfully!", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Sector deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )
class BigSectorViewSet(viewsets.ModelViewSet):
    queryset = BigSector.objects.all()
    serializer_class = BigSectorSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Sector created successfully!", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Sector updated successfully!", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Sector deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )
class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Vehicle Type created successfully!", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Vehicle Type updated successfully!", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Vehicle Type deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )
class InternalNoteViewSet(viewsets.ModelViewSet):
    queryset = InternalNote.objects.all().order_by("-date_time")
    serializer_class = InternalNoteSerializer
class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all().order_by("-id")
    serializer_class = BankAccountSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # ðŸ‘ˆ yahan save zaroori hai
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class OrganizationLinkViewSet(viewsets.ModelViewSet):
    queryset = OrganizationLink.objects.all()
    serializer_class = OrganizationLinkSerializer

    def create(self, request, *args, **kwargs):
        # agar array aya hai
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
class AllowedResellerViewSet(viewsets.ModelViewSet):
    queryset = AllowedReseller.objects.all()
    serializer_class = AllowedResellerSerializer

class DiscountGroupViewSet(viewsets.ModelViewSet):
    queryset = DiscountGroup.objects.all().prefetch_related("discounts")
    serializer_class = DiscountGroupSerializer
class MarkupViewSet(viewsets.ModelViewSet):
    queryset = Markup.objects.all().order_by("-created_at")
    serializer_class = MarkupSerializer
from rest_framework import viewsets,status
from django.db.models import Prefetch, Sum, F, Value, DecimalField,FloatField
from django.db.models.functions import Coalesce, Round,Cast
from rest_framework.decorators import action
from django.db import connection
from django.db import models
from rest_framework.permissions import BasePermission

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
    Markup
)
from .serializers import BookingSerializer, PaymentSerializer, SectorSerializer, BigSectorSerializer, VehicleTypeSerializer, InternalNoteSerializer, DiscountGroupSerializer, BankAccountSerializer, OrganizationLinkSerializer, AllowedResellerSerializer, MarkupSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

import json
class BookingViewSet(viewsets.ModelViewSet):
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


    def create(self, request, *args, **kwargs):
        normalized = self._normalize_data(request)
        serializer = self.get_serializer(data=normalized)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        normalized = self._normalize_data(request.data)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=normalized, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.select_related(
            "organization", "branch", "agency", "agent", "created_by", "booking", "bank"
        ).order_by("-date")
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
    
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
class OrganizationLinkViewSet(viewsets.ModelViewSet):
    queryset = OrganizationLink.objects.all()
    serializer_class = OrganizationLinkSerializer
    permission_classes=[IsSuperAdmin]

    def create(self, request, *args, **kwargs):
        # agar array aya hai
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    @action(detail=False, methods=['get'], url_path='shared')
    def shared_inventory_partners(self, request):
        """
        Returns only those organization links where both sides
        have accepted (shared inventory active).
        """
        org_id = request.query_params.get('organization_id')
        if not org_id:
            return Response({"error": "organization_id is required"}, status=400)

        links = OrganizationLink.objects.filter(
            models.Q(main_organization_id=org_id) |
            models.Q(linked_organization_id=org_id),
            main_organization_request="ACCEPTED",
            this_organization_request="ACCEPTED"
        )

        serializer = self.get_serializer(links, many=True)
        return Response(serializer.data)
class AllowedResellerViewSet(viewsets.ModelViewSet):
    queryset = AllowedReseller.objects.all()
    serializer_class = AllowedResellerSerializer

class DiscountGroupViewSet(viewsets.ModelViewSet):
    queryset = DiscountGroup.objects.all().prefetch_related("discounts")
    serializer_class = DiscountGroupSerializer
class MarkupViewSet(viewsets.ModelViewSet):
    queryset = Markup.objects.all().order_by("-created_at")
    serializer_class = MarkupSerializer
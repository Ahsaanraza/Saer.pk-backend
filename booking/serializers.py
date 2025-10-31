from rest_framework import serializers
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now
from organization.serializers import OrganizationSerializer,AgencySerializer, BranchSerializer
from packages.serializers import RiyalRateSerializer, UmrahPackageSerializer
from tickets.serializers import HotelsSerializer
from users.serializers import UserSerializer
from organization.models import Organization, Agency, Branch
from users.models import UserProfile
from tickets.models import Hotels
from datetime import datetime
from decimal import Decimal
from .models import (
    Booking,
    BookingHotelDetails,
    BookingTransportDetails,
    BookingTicketDetails,
    BookingTicketTicketTripDetails,
    BookingTicketStopoverDetails,
    BookingPersonZiyaratDetails,
    BookingPersonFoodDetails,
    BookingPersonDetail,
    BookingPersonContactDetails,
    Payment,
    Sector,
    BigSector,
    VehicleType,
    InternalNote,
    BookingTransportSector,
    BankAccount,
    OrganizationLink,
    AllowedReseller,
    DiscountGroup,
    Discount,
    Markup,
    BookingCallRemark
)
from django.db import transaction

# --- Public (read-only) serializers for the public booking status API ---
class PublicPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPersonDetail
        fields = (
            "person_title",
            "first_name",
            "last_name",
            "age_group",
            "passport_number",
            "date_of_birth",
        )


class PublicHotelDetailsSerializer(serializers.ModelSerializer):
    # show related hotel basic info if available
    hotel = HotelsSerializer(read_only=True)

    class Meta:
        model = BookingHotelDetails
        fields = (
            "hotel",
            "self_hotel_name",
            "check_in_date",
            "check_out_date",
            "number_of_nights",
            "room_type",
            "sharing_type",
        )


class PublicTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTransportDetails
        fields = (
            "shirka",
            "vehicle_type",
            "voucher_no",
            "brn_no",
        )


class PublicTicketSerializer(serializers.ModelSerializer):
    trip_details = serializers.SerializerMethodField()

    class Meta:
        model = BookingTicketDetails
        fields = (
            "pnr",
            "trip_details",
            "seats",
            "status",
        )

    def get_trip_details(self, obj):
        out = []
        try:
            for t in getattr(obj, 'trip_details').all():
                out.append({
                    'departure_date_time': t.departure_date_time,
                    'arrival_date_time': t.arrival_date_time,
                    'departure_city': getattr(t.departure_city, 'name', None) if getattr(t, 'departure_city', None) else None,
                    'arrival_city': getattr(t.arrival_city, 'name', None) if getattr(t, 'arrival_city', None) else None,
                    'trip_type': t.trip_type,
                })
        except Exception:
            pass
        return out


class PublicBookingSerializer(serializers.ModelSerializer):
    person_details = PublicPersonSerializer(many=True, read_only=True)
    hotel_details = PublicHotelDetailsSerializer(many=True, read_only=True)
    transport_details = PublicTransportSerializer(many=True, read_only=True)
    ticket_details = PublicTicketSerializer(many=True, read_only=True)
    public_ref = serializers.CharField(read_only=True)
    booking_number = serializers.CharField(read_only=True)
    creation_date = serializers.DateTimeField(source="date", read_only=True)
    service_summary = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    remaining_balance = serializers.SerializerMethodField()
    uploaded_documents = serializers.SerializerMethodField()
    status_timeline = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = (
            "booking_number",
            "public_ref",
            "creation_date",
            "person_details",
            "service_summary",
            "booking_type",
            "hotel_details",
            "transport_details",
            "ticket_details",
            "payment_status",
            "status",
            "total_paid",
            "remaining_balance",
            "uploaded_documents",
        )

    def get_service_summary(self, obj):
        # Minimal public-facing summary
        out = {
            "booking_type": obj.booking_type,
            "category": obj.category,
            "is_full_package": obj.is_full_package,
        }
        # package name/duration
        try:
            if getattr(obj, 'umrah_package', None):
                out['package_name'] = getattr(obj.umrah_package, 'title', None) or getattr(obj.umrah_package, 'name', None)
                # approximate duration from hotel nights
                nights = 0
                for h in getattr(obj, 'hotel_details').all():
                    nights += int(getattr(h, 'number_of_nights', 0) or 0)
                out['duration_nights'] = nights
        except Exception:
            pass

        # hotel names and transport summary
        try:
            hotels = []
            for h in getattr(obj, 'hotel_details').all():
                hotels.append(h.self_hotel_name or (getattr(h.hotel, 'name', None) if getattr(h, 'hotel', None) else None))
            out['hotel_names'] = [x for x in hotels if x]
        except Exception:
            out['hotel_names'] = []

        try:
            transports = []
            for t in getattr(obj, 'transport_details').all():
                transports.append({
                    'vehicle_type': getattr(t, 'vehicle_type', None),
                    'voucher_no': getattr(t, 'voucher_no', None),
                })
            out['transport_summary'] = transports
        except Exception:
            out['transport_summary'] = []

        # visa status (public-facing)
        try:
            out['visa_status'] = getattr(obj, 'visa_status', None)
        except Exception:
            out['visa_status'] = None

        return out

    def get_status_timeline(self, obj):
        timeline = []
        try:
            # Booked
            timeline.append({'status': 'booked', 'at': getattr(obj, 'date', None)})
            # Payments (completed)
            if hasattr(obj, 'payment_details'):
                for p in obj.payment_details.filter(status__in=['Completed', 'completed']):
                    timeline.append({'status': 'paid', 'at': getattr(p, 'date', None), 'amount': float(getattr(p, 'amount', 0) or 0)})
            # Confirmed
            if getattr(obj, 'status', None) and str(getattr(obj, 'status')).lower() == 'confirmed':
                # use last payment date or booking date as proxy
                last_paid = None
                try:
                    last_paid = obj.payment_details.filter(status__in=['Completed', 'completed']).order_by('-date').first()
                except Exception:
                    last_paid = None
                timeline.append({'status': 'confirmed', 'at': getattr(last_paid, 'date', None) or getattr(obj, 'date', None)})
        except Exception:
            pass
        return timeline

    def get_total_paid(self, obj):
        # try fields on model first, fall back to summing payments
        try:
            if getattr(obj, "paid_payment", None) not in (None, ""):
                return float(obj.paid_payment or 0)
            # try JSON payments
            if isinstance(obj.payments, (list, tuple)) and obj.payments:
                return sum([float(p.get("amount", 0) or 0) for p in obj.payments])
            # try related payment_details
            if hasattr(obj, "payment_details"):
                return sum([float(p.amount or 0) for p in obj.payment_details.all()])
        except Exception:
            return 0.0
        return 0.0

    def get_remaining_balance(self, obj):
        try:
            if getattr(obj, "pending_payment", None) not in (None, ""):
                return float(obj.pending_payment or 0)
            total = float(obj.total_amount or 0)
            paid = float(self.get_total_paid(obj) or 0)
            return max(0.0, total - paid)
        except Exception:
            return None

    def get_uploaded_documents(self, obj):
        # Return a minimal list of uploaded document info if available. Defensive — do not expose internal paths.
        docs = []
        try:
            # example: look for voucher / passport fields on booking or persons
            # Booking may store attachments in JSON fields; fall back to person passport_picture
            if hasattr(obj, "person_details"):
                for p in obj.person_details.all():
                    if getattr(p, "passport_picture", None):
                        docs.append({"type": "passport_picture", "filename": getattr(p.passport_picture, "name", None), "url": getattr(p.passport_picture, "url", None)})
            # Booking-level attachments could exist in journal_items/payments — skip those for privacy
        except Exception:
            pass
        return docs


# --- Public (write) serializers for creating bookings/payments ---
class PublicBookingCreateSerializer(serializers.Serializer):
    umrah_package_id = serializers.IntegerField()
    total_pax = serializers.IntegerField()
    total_adult = serializers.IntegerField(required=False, default=0)
    total_child = serializers.IntegerField(required=False, default=0)
    total_infant = serializers.IntegerField(required=False, default=0)
    contact_name = serializers.CharField(max_length=255)
    contact_phone = serializers.CharField(max_length=50)
    contact_email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    pay_now = serializers.BooleanField(required=False, default=False)
    pay_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    def validate(self, data):
        from packages.models import UmrahPackage

        try:
            pkg = UmrahPackage.objects.get(pk=data['umrah_package_id'])
        except UmrahPackage.DoesNotExist:
            raise serializers.ValidationError({"umrah_package_id": "Invalid package id"})

        if not pkg.is_public:
            raise serializers.ValidationError({"umrah_package_id": "Package is not available for public booking"})

        total = int(data.get('total_pax') or 0)
        left = int(pkg.left_seats or 0)
        if total <= 0:
            raise serializers.ValidationError({"total_pax": "Must be greater than zero"})
        if left < total:
            raise serializers.ValidationError({"total_pax": f"Only {left} seats left"})

        return data

    class Meta:
        fields = '__all__'


class PublicPaymentCreateSerializer(serializers.Serializer):
    booking_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    method = serializers.CharField(max_length=50, default="online")
    transaction_number = serializers.CharField(max_length=128, required=False, allow_blank=True, allow_null=True)

    def validate(self, data):
        from .models import Booking

        try:
            Booking.objects.get(booking_number=data['booking_number'])
        except Booking.DoesNotExist:
            raise serializers.ValidationError({"booking_number": "Invalid booking_number"})
        return data

    class Meta:
        fields = '__all__'

# --- Child serializers ---


class BookingTicketTripDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTicketTicketTripDetails
        fields = "__all__"
        extra_kwargs = {"ticket": {"read_only": True}}


class BookingTicketStopoverDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTicketStopoverDetails
        fields = "__all__"
        extra_kwargs = {"ticket": {"read_only": True}}


class BookingTicketDetailsSerializer(serializers.ModelSerializer):
    trip_details = BookingTicketTripDetailsSerializer(many=True, required=False)
    stopover_details = BookingTicketStopoverDetailsSerializer(many=True, required=False)

    class Meta:
        model = BookingTicketDetails
        fields = "__all__"
        extra_kwargs = {"booking": {"read_only": True}}

    def create(self, validated_data):
        trip_data = validated_data.pop("trip_details", [])
        stopover_data = validated_data.pop("stopover_details", [])
        ticket = BookingTicketDetails.objects.create(**validated_data)

        if trip_data:
                BookingTicketTicketTripDetails.objects.bulk_create(
                    [
                        BookingTicketTicketTripDetails(
                            ticket=ticket,
                            departure_city=td["departure_city"],
                            arrival_city=td["arrival_city"],
                            departure_date_time=td["departure_date_time"],
                            arrival_date_time=td["arrival_date_time"],
                            trip_type=td["trip_type"],
                        )
                        for td in trip_data
                    ]
                )
      # Stopover Details
        if stopover_data:
            BookingTicketStopoverDetails.objects.bulk_create(
                [
                    BookingTicketStopoverDetails(
                        ticket=ticket,
                        stopover_city=sd["stopover_city"],
                        stopover_duration=sd["stopover_duration"],
                        trip_type=sd["trip_type"],
                    )
                    for sd in stopover_data
                ]
            )

        return ticket

    def update(self, instance, validated_data):
        trip_data = validated_data.pop("trip_details", [])
        stopover_data = validated_data.pop("stopover_details", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


        if trip_data is not None:
            instance.trip_details.all().delete()
            BookingTicketTicketTripDetails.objects.bulk_create(
                [
                    BookingTicketTicketTripDetails(
                        ticket=instance,
                        departure_city=td["departure_city"],
                        arrival_city=td["arrival_city"],
                        departure_date_time=td["departure_date_time"],
                        arrival_date_time=td["arrival_date_time"],
                        trip_type=td["trip_type"],
                    )
                    for td in trip_data
                ]
            )
        if stopover_data is not None:
            instance.stopover_details.all().delete()
            BookingTicketStopoverDetails.objects.bulk_create(
                [
                    BookingTicketStopoverDetails(
                        ticket=instance,
                        stopover_city=sd["stopover_city"],
                        stopover_duration=sd["stopover_duration"],
                        trip_type=sd["trip_type"],
                    )
                    for sd in stopover_data
                ]
            )
        return instance


class BookingHotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHotelDetails
        fields = "__all__"
        extra_kwargs = {"booking": {"read_only": True}}

class BookingTransportSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingTransportSector
        fields = "__all__"
        extra_kwargs = {
            "transport_detail": {"read_only": True}
        }

# class BookingTransportDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookingTransportDetails
#         fields = "__all__"
#         extra_kwargs = {"booking": {"read_only": True}}
class BookingTransportDetailsSerializer(serializers.ModelSerializer):
    sector_details = BookingTransportSectorSerializer(many=True, required=False)

    class Meta:
        model = BookingTransportDetails
        fields = "__all__"
        extra_kwargs = {"booking": {"read_only": True}}

    def create(self, validated_data):
        # pop nested data
        sector_data = validated_data.pop("sector_details", [])
        transport_detail = BookingTransportDetails.objects.create(**validated_data)

        # create nested sector records
        for sector in sector_data:
            BookingTransportSector.objects.create(
                transport_detail=transport_detail, **sector
            )

        return transport_detail

    def update(self, instance, validated_data):
        # update main fields
        sector_data = validated_data.pop("sector_details", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # handle nested update
        if sector_data is not None:
            instance.sector_details.all().delete()
            for sector in sector_data:
                BookingTransportSector.objects.create(
                    transport_detail=instance, **sector
                )
        return instance


class BookingPersonZiyaratDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPersonZiyaratDetails
        fields = "__all__"
        extra_kwargs = {"person": {"read_only": True}}
class BookingPersonFoodDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPersonFoodDetails
        fields = "__all__"
        extra_kwargs = {"person": {"read_only": True}}
class BookingPersonContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPersonContactDetails
        fields = "__all__"
        extra_kwargs = {"person": {"read_only": True}}

class BookingPersonDetailSerializer(serializers.ModelSerializer):
    # contact_details = BookingPersonContactDetailsSerializer(many=True, required=False)
    class Meta:
        model = BookingPersonDetail
        fields = "__all__"
        extra_kwargs = {"booking": {"read_only": True}}
    
    def create(self, validated_data):
        # nested lists
        ziyarat_data = validated_data.pop("ziyarat_details", [])
        food_data = validated_data.pop("food_details", [])
        contact_data = validated_data.pop("contact_details", [])
        person = BookingPersonDetail.objects.create(**validated_data)

        if ziyarat_data:
            BookingPersonZiyaratDetails.objects.bulk_create(
                [BookingPersonZiyaratDetails(person=person, **zd) for zd in ziyarat_data]
            )
        if food_data:
            BookingPersonFoodDetails.objects.bulk_create(
                [BookingPersonFoodDetails(person=person, **fd) for fd in food_data]
            )
        if contact_data:
            BookingPersonContactDetails.objects.bulk_create(
                [BookingPersonContactDetails(person=person, **cd) for cd in contact_data]
            )
        return person
    
    def update(self, instance, validated_data):
        # nested lists (None if not provided on PATCH)
        ziyarat_data = validated_data.pop("ziyarat_details", None)
        food_data = validated_data.pop("food_details", None)
        contact_data = validated_data.pop("contact_details", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if ziyarat_data is not None:
            # instance.ziyarat_details.all().delete()
            BookingPersonZiyaratDetails.objects.bulk_create(
                [BookingPersonZiyaratDetails(person=instance, **zd) for zd in ziyarat_data]
            )
        if food_data is not None:
            instance.food_details.all().delete()
            BookingPersonFoodDetails.objects.bulk_create(
                [BookingPersonFoodDetails(person=instance, **fd) for fd in food_data]
            )
        if contact_data is not None:
            instance.contact_details.all().delete()
            BookingPersonContactDetails.objects.bulk_create(
                [BookingPersonContactDetails(person=instance, **cd) for cd in contact_data]
            )
        return instance
    


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {"booking": {"read_only": True}}


class HotelOutsourcingSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), source='booking', write_only=True)
    booking_hotel_detail_id = serializers.PrimaryKeyRelatedField(queryset=BookingHotelDetails.objects.all(), source='booking_hotel_detail', required=False, allow_null=True, write_only=True)
    outsource_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = None  # placeholder; we will import locally to avoid circular imports
        fields = [
            'id', 'booking_id', 'booking_hotel_detail_id', 'hotel_name', 'source_company', 'check_in_date', 'check_out_date',
            'room_type', 'room_no', 'price', 'quantity', 'number_of_nights', 'currency', 'remarks', 'is_paid', 'agent_notified',
            'created_by', 'created_at', 'updated_at', 'is_deleted', 'outsource_cost', 'ledger_entry_id'
        ]

    def __init__(self, *args, **kwargs):
        # avoid circular import issues by binding model at runtime
        from .models import HotelOutsourcing
        self.Meta.model = HotelOutsourcing
        super().__init__(*args, **kwargs)

    def get_outsource_cost(self, obj):
        return obj.outsource_cost

    def create(self, validated_data):
        from .models import HotelOutsourcing
        from django.db import transaction

        booking = validated_data.get('booking')
        booking_hotel_detail = validated_data.get('booking_hotel_detail', None)

        with transaction.atomic():
            ho = HotelOutsourcing.objects.create(**validated_data)

            # mark booking as outsourced
            booking.is_outsourced = True
            booking.save(update_fields=['is_outsourced'])

            # update booking hotel detail if provided
            if booking_hotel_detail:
                booking_hotel_detail.self_hotel_name = ho.hotel_name
                booking_hotel_detail.check_in_date = ho.check_in_date or booking_hotel_detail.check_in_date
                booking_hotel_detail.check_out_date = ho.check_out_date or booking_hotel_detail.check_out_date
                booking_hotel_detail.room_type = ho.room_type or booking_hotel_detail.room_type
                booking_hotel_detail.outsourced_hotel = True
                booking_hotel_detail.save()

        return ho

    def update(self, instance, validated_data):
        # allow patching payment status and agent_notified only via serializer
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance


# --- Main Booking Serializer ---
class BookingSerializer(serializers.ModelSerializer):
    umrah_package = UmrahPackageSerializer(read_only=True)
    ziyarat_details = BookingPersonZiyaratDetailsSerializer(many=True, required=False)
    food_details = BookingPersonFoodDetailsSerializer(many=True, required=False)
    agency_id = serializers.PrimaryKeyRelatedField(
        queryset=Agency.objects.all(), source="agency"
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), source="user"
    )
    internal_notes_id = serializers.PrimaryKeyRelatedField(
        source="internal",
        queryset=InternalNote.objects.all(),
        write_only=True
    )
    hotel_details = BookingHotelDetailsSerializer(many=True, required=False)
    transport_details = BookingTransportDetailsSerializer(many=True, required=False)
    ticket_details = BookingTicketDetailsSerializer(many=True, required=False)
    person_details = BookingPersonDetailSerializer(many=True, required=False)
    payment_details = PaymentSerializer(many=True, required=False)
    payments = serializers.ListField(child=serializers.DictField(), required=False)
    journal_items = serializers.ListField(child=serializers.DictField(), required=False)
    remaining_amount = serializers.FloatField(read_only=True)
    booking_number = serializers.CharField(read_only=True)
    agency = AgencySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    confirmed_by = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # ✅ Food array sirf tab show hoga jab flag true hai
        if not instance.is_food_included:
            data.pop("food_details", None)

        # ✅ Ziyarat array sirf tab show hoga jab flag true hai
        if not instance.is_ziyarat_included:
            data.pop("ziyarat_details", None)

        return data
    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("booking_number", None)
        hotel_data = validated_data.pop("hotel_details", [])
        transport_data = validated_data.pop("transport_details", [])
        ticket_data = validated_data.pop("ticket_details", [])
        person_data = validated_data.pop("person_details", [])
        payment_data = validated_data.pop("payment_details", [])
        payments_data = validated_data.pop("payments", [])
        journal_data = validated_data.pop("journal_items", [])

        booking_number = f"BK-{now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        # booking = Booking.objects.create(**validated_data)
        booking = Booking.objects.create(
            booking_number=booking_number,
            **validated_data
        )

        # attach payments/journal if provided (stored as JSON on Booking)
        if payments_data:
            booking.payments = payments_data
        if journal_data:
            booking.journal_items = journal_data
        booking.save()

        # --- Flat relations (bulk_create) ---
        # if hotel_data:
        #     BookingHotelDetails.objects.bulk_create(
        #         [BookingHotelDetails(booking=booking, **hd) for hd in hotel_data]
        #     )
        from packages.models import RiyalRate  # apni app ka naam dalna
        rate_obj = RiyalRate.objects.filter(organization=booking.organization).first()
        hotel_instances = []
        total_pkr_sum = 0
        total_riyal_sum = 0
        for hd in hotel_data:
            check_in = hd["check_in_date"]
            check_out = hd["check_out_date"]
            

            nights = (check_out - check_in).days
            if nights < 0:
                nights = 0  

            price = hd.get("price", 0)
            quantity = hd.get("quantity", 1)

            total_price = price * nights * quantity
            hd["number_of_nights"] = nights
            hd["total_price"] = total_price
            if rate_obj and rate_obj.is_hotel_pkr is False:
                hd["total_in_riyal_rate"] = total_price
                hd["total_in_pkr"] = total_price * rate_obj.rate
                total_riyal_sum += hd["total_in_riyal_rate"]
                total_pkr_sum += hd["total_in_pkr"]
            else:
                hd["total_in_riyal_rate"] = None
                hd["total_in_pkr"] = None
            hotel_instances.append(BookingHotelDetails(booking=booking, **hd))
        if hotel_instances:
            BookingHotelDetails.objects.bulk_create(hotel_instances)
        booking.total_hotel_amount_pkr = total_pkr_sum
        booking.total_hotel_amount_sar = total_riyal_sum
        booking.save()
        # if transport_data:
        #     BookingTransportDetails.objects.bulk_create(
        #         [BookingTransportDetails(booking=booking, **td) for td in transport_data]
        #     )
        # if transport_data:
        #     for td in transport_data:
        #         # extract nested sectors
        #         sector_data = td.pop("sector_details", [])
        
        #         # create transport detail
        #         transport_detail = BookingTransportDetails.objects.create(
        #             booking=booking, **td
        #         )
        
        #         # create related sector rows
        #         for sd in sector_data:
        #             BookingTransportSector.objects.create(
        #                 transport_detail=transport_detail, **sd
        #             )
        if transport_data:
            from packages.models import RiyalRate  
            from decimal import Decimal
            
            rate_obj = RiyalRate.objects.filter(organization=booking.organization).first()
        
            for td in transport_data:
                sector_data = td.pop("sector_details", [])
        
                # --- vehicle_type ki price le kar td me dal do ---
                vehicle_type = td.get("vehicle_type")
                price_value = 0
                if vehicle_type:
                    try:
                        vt = VehicleType.objects.get(id=vehicle_type.id if hasattr(vehicle_type, "id") else vehicle_type)
                        price_value = vt.price
                    except VehicleType.DoesNotExist:
                        price_value = 0
        
                td["price"] = price_value  
        
                # --- conversion logic ---
                if rate_obj and td.get("is_price_pkr") is False:
                    base_price = Decimal(str(td.get("price", 0)))  # float -> decimal safe conversion
                    riyal_rate = Decimal(str(rate_obj.rate)) if rate_obj else Decimal("0")
                    td["price_in_sar"] = base_price
                    td["price_in_pkr"] = base_price * riyal_rate
                    td["riyal_rate"] = riyal_rate
                else:
                    td["price_in_pkr"] = price_value

                # create transport detail
                transport_detail = BookingTransportDetails.objects.create(
                    booking=booking, **td
                )
        
                # create related sector rows
                for sd in sector_data:
                    BookingTransportSector.objects.create(
                        transport_detail=transport_detail, **sd
                    )

    
        # --- Nested tickets (delegate to serializer) ---
        for td in ticket_data:
            serializer = BookingTicketDetailsSerializer()
            serializer.create({**td, "booking": booking})

        # --- Nested persons (delegate to serializer) ---
        for pd in person_data:
            serializer = BookingPersonDetailSerializer(data=pd)
            serializer.is_valid(raise_exception=True)
            serializer.save(booking=booking)

        # --- Flat payments ---
        if payment_data:
            Payment.objects.bulk_create(
                [Payment(booking=booking, **pay) for pay in payment_data]
            )

        return booking

    @transaction.atomic
    def update(self, instance, validated_data):
        hotel_data = validated_data.pop("hotel_details", [])
        transport_data = validated_data.pop("transport_details", [])
        ticket_data = validated_data.pop("ticket_details", [])
        person_data = validated_data.pop("person_details", [])
        payment_data = validated_data.pop("payment_details", [])

        # update booking fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # --- Hotels ---
        if hotel_data is not None:
            instance.hotel_details.all().delete()
            BookingHotelDetails.objects.bulk_create(
                [BookingHotelDetails(booking=instance, **hd) for hd in hotel_data]
            )

        # --- Transport ---
        if transport_data is not None:
            instance.transport_details.all().delete()
            BookingTransportDetails.objects.bulk_create(
                [BookingTransportDetails(booking=instance, **td) for td in transport_data]
            )

        # --- Tickets ---
        if ticket_data is not None:
            instance.ticket_details.all().delete()
            for td in ticket_data:
                serializer = BookingTicketDetailsSerializer(data=td)
                serializer.is_valid(raise_exception=True)
                serializer.save(booking=instance)

        # --- Persons ---
        if person_data is not None:
            instance.person_details.all().delete()
            for pd in person_data:
                serializer = BookingPersonDetailSerializer(data=pd)
                serializer.is_valid(raise_exception=True)
                serializer.save(booking=instance)

        # --- Payments ---
        if payment_data is not None:
            instance.payment_details.all().delete()
            Payment.objects.bulk_create(
                [Payment(booking=instance, **pay) for pay in payment_data]
            )

        return instance



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"
class BigSectorSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source="organization",
        write_only=True
    )
    # Nested read
    small_sectors = SectorSerializer(many=True, read_only=True)
    # IDs write
    small_sector_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Sector.objects.all(),
        source="small_sectors",
        write_only=True
    )

    class Meta:
        model = BigSector
        fields = [
            "id",
            "organization", "organization_id",
            "small_sectors", "small_sector_ids",
        ]

    def create(self, validated_data):
        small_sectors = validated_data.pop("small_sectors", [])
        big_sector = BigSector.objects.create(**validated_data)
        if small_sectors:
            big_sector.small_sectors.set(small_sectors)
        return big_sector

    def update(self, instance, validated_data):
        small_sectors = validated_data.pop("small_sectors", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if small_sectors is not None:
            instance.small_sectors.set(small_sectors)
        return instance
class VehicleTypeSerializer(serializers.ModelSerializer):
    small_sector = SectorSerializer(read_only=True)
    small_sector_id = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.all(), source="small_sector", write_only=True, required=False, allow_null=True
    )

    big_sector = BigSectorSerializer(read_only=True)
    big_sector_id = serializers.PrimaryKeyRelatedField(
        queryset=BigSector.objects.all(), source="big_sector", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = VehicleType
        fields = [
            "id",
            "vehicle_name",
            "vehicle_type",
            "price",
            "note",
            "visa_type",
            "status",
            "organization",
            "small_sector",
            "small_sector_id",
            "big_sector",
            "big_sector_id",
        ]
class InternalNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalNote
        fields = "__all__"
class BankAccountSerializer(serializers.ModelSerializer):
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), source="organization", write_only=True
    )
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), source="branch", write_only=True
    )
    agency_id = serializers.PrimaryKeyRelatedField(
        queryset=Agency.objects.all(), source="agency", write_only=True, required=False, allow_null=True
    )

    organization = OrganizationSerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    agency = AgencySerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = "__all__"
    def create(self, validated_data):
        organization = validated_data.pop("organization")
        branch = validated_data.pop("branch")
        agency = validated_data.pop("agency")
        
        return BankAccount.objects.create(
            organization=organization,
            branch=branch,
            agency=agency,
            **validated_data
        )
class OrganizationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationLink
        fields = "__all__"
class AllowedResellerSerializer(serializers.ModelSerializer):
    reseller_company = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), allow_null=True, required=False
    )
    discount_group = serializers.PrimaryKeyRelatedField(
        queryset=DiscountGroup.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = AllowedReseller
        # expose only relevant fields in stable order
        fields = [
            "id",
            "inventory_owner_company",
            "reseller_company",
            "discount_group",
            "allowed_types",
            "requested_status_by_reseller",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        # inventory_owner_company, reseller_company, discount_group, allowed_types
        return AllowedReseller.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
class DiscountSerializer(serializers.ModelSerializer):
    discounted_hotels = serializers.PrimaryKeyRelatedField(
        queryset=Hotels.objects.all(), many=True, write_only=True, required=False
    )
    discounted_hotels_data = HotelsSerializer(
        many=True, read_only=True, source="discounted_hotels"
    )

    class Meta:
        model = Discount
        fields = [
            "id",
            "organization",
            "things",
            "group_ticket_discount_amount",
            "umrah_package_discount_amount",
            "currency",
            "room_type",
            "per_night_discount",
            "discounted_hotels",       # POST/PUT ke liye IDs
            "discounted_hotels_data",  # GET ke liye full objects
        ]


class DiscountGroupSerializer(serializers.ModelSerializer):
    # discounts are accepted on write, but for GET we return a compact object (see to_representation)
    discounts = DiscountSerializer(many=True, write_only=True, required=False)

    # allow a more convenient hotel_night_discounts payload shape as requested by the API (write-only)
    hotel_night_discounts = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = DiscountGroup
        fields = ["id", "name", "group_type", "organization", "is_active", "discounts", "hotel_night_discounts"]

    def create(self, validated_data):
        discounts_data = validated_data.pop("discounts", [])
        hotel_night_discounts = validated_data.pop("hotel_night_discounts", [])
        discount_group = DiscountGroup.objects.create(**validated_data)

        # create explicit discounts passed in the `discounts` list
        for discount_data in discounts_data:
            hotels = discount_data.pop("discounted_hotels", [])
            discount = Discount.objects.create(discount_group=discount_group, **discount_data)
            if hotels:
                discount.discounted_hotels.set(hotels)

        # handle hotel_night_discounts convenience format: each entry may contain per-room-type discounts + discounted_hotels list
        # expected keys: quint_per_night_discount, quad_per_night_discount, triple_per_night_discount, double_per_night_discount, sharing_per_night_discount, other_per_night_discount, discounted_hotels
        room_map = {
            "quint_per_night_discount": "quint",
            "quad_per_night_discount": "quad",
            "triple_per_night_discount": "triple",
            "double_per_night_discount": "double",
            "sharing_per_night_discount": "sharing",
            "other_per_night_discount": "all",
        }

        for entry in hotel_night_discounts:
            hotels = entry.get("discounted_hotels", [])
            for key, room_type in room_map.items():
                val = entry.get(key)
                if val in (None, "", []):
                    continue
                # create a Discount per room type
                disc = Discount.objects.create(
                    discount_group=discount_group,
                    organization=discount_group.organization,
                    things="hotel",
                    room_type=room_type,
                    per_night_discount=val,
                )
                if hotels:
                    disc.discounted_hotels.set(hotels)

        return discount_group

    def to_representation(self, instance):
        # Build discounts object (single values)
        group_ticket_disc = instance.discounts.filter(things="group_ticket").first()
        umrah_disc = instance.discounts.filter(things="umrah_package").first()

        discounts_obj = {
            "group_ticket_discount_amount": (
                str(group_ticket_disc.group_ticket_discount_amount)
                if group_ticket_disc and group_ticket_disc.group_ticket_discount_amount is not None
                else ""
            ),
            "umrah_package_discount_amount": (
                str(umrah_disc.umrah_package_discount_amount)
                if umrah_disc and umrah_disc.umrah_package_discount_amount is not None
                else ""
            ),
        }

        # Build hotel_night_discounts list by grouping hotel Discounts by the set of hotel IDs
        hotel_discs = instance.discounts.filter(things="hotel").prefetch_related("discounted_hotels")
        grouped = {}
        room_key_map = {
            "quint": "quint_per_night_discount",
            "quad": "quad_per_night_discount",
            "triple": "triple_per_night_discount",
            "double": "double_per_night_discount",
            "sharing": "sharing_per_night_discount",
            "all": "other_per_night_discount",
        }

        # helper to format hotel per-night discounts: drop ".00" for whole numbers
        def _fmt_hotel_amount(val):
            if val is None:
                return ""
            try:
                dec = Decimal(str(val))
            except Exception:
                return str(val)
            # integer value → return without decimal part
            if dec == dec.to_integral():
                return str(int(dec))
            # otherwise remove trailing zeros
            return format(dec.normalize(), 'f')

        for disc in hotel_discs:
            hotel_ids = tuple(sorted([h.id for h in disc.discounted_hotels.all()]))
            if hotel_ids not in grouped:
                grouped[hotel_ids] = {
                    "quint_per_night_discount": "",
                    "quad_per_night_discount": "",
                    "triple_per_night_discount": "",
                    "double_per_night_discount": "",
                    "sharing_per_night_discount": "",
                    "other_per_night_discount": "",
                    "discounted_hotels": list(hotel_ids),
                }

            key = room_key_map.get(disc.room_type)
            if key:
                grouped[hotel_ids][key] = _fmt_hotel_amount(disc.per_night_discount)

        # Return an explicit minimal representation so no extra keys are included
        return {
            "id": instance.id,
            "name": instance.name,
            "group_type": instance.group_type,
            "organization": instance.organization_id,
            "is_active": instance.is_active,
            "discounts": discounts_obj,
            "hotel_night_discounts": list(grouped.values()),
        }
class MarkupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markup
        fields = [
            "id",
            "name",
            "applies_to",
            "ticket_markup",
            "hotel_per_night_markup",
            "umrah_package_markup",
            "organization_id",
            "created_at",
            "updated_at",
        ]

class BookingCallRemarkSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="created_by", write_only=True, required=False
    )

    class Meta:
        model = BookingCallRemark
        fields = [
            "id",
            "booking",
            "created_by",
            "created_by_id",
            "remark_text",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


from rest_framework import serializers
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
    Markup
)
from django.db import transaction

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
    discounts = DiscountSerializer(many=True, required=False)

    # allow a more convenient hotel_night_discounts payload shape as requested by the API
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
        """
        Return the requested API shape:
        - `discounts` as an object with `group_ticket_discount_amount` and `umrah_package_discount_amount` keys
        - `hotel_night_discounts` as a list of objects where each object contains per-room-type keys and `discounted_hotels` list
        """
        data = super().to_representation(instance)

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
        data["discounts"] = discounts_obj

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

        # For each hotel discount row, associate its per_night_discount under the correct grouping
        for disc in hotel_discs:
            hotel_ids = tuple(sorted([h.id for h in disc.discounted_hotels.all()]))
            if hotel_ids not in grouped:
                # initialize an entry with empty strings
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
                grouped[hotel_ids][key] = (
                    str(disc.per_night_discount) if disc.per_night_discount is not None else ""
                )

        data["hotel_night_discounts"] = list(grouped.values())

        return data
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


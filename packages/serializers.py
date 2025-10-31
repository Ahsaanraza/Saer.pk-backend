from rest_framework.serializers import ModelSerializer
from organization.serializers import OrganizationSerializer
from .models import City
from booking.models import VehicleType
from users.serializers import UserSerializer
from .models import (
    RiyalRate,
    Shirka,
    UmrahVisaPrice,
    UmrahVisaPriceTwo,
    UmrahVisaPriceTwoHotel,
    TransportSectorPrice,
    Airlines,
    City,
    BookingExpiry,
    UmrahPackage,
    UmrahPackageHotelDetails,
    UmrahPackageTransportDetails,
    UmrahPackageTicketDetails,
    UmrahPackageDiscountDetails,
    CustomUmrahPackage,
    CustomUmrahPackageHotelDetails,
    CustomUmrahPackageTransportDetails,
    CustomUmrahPackageTicketDetails,
    CustomUmrahZiaratDetails,
    CustomUmrahFoodDetails,
    OnlyVisaPrice,
    SetVisaType,
    FoodPrice,
    ZiaratPrice,
)
from rest_framework import serializers
from tickets.serializers import HotelsSerializer, TicketSerializer
from django.db import models


class RiyalRateSerializer(ModelSerializer):
    class Meta:
        model = RiyalRate
        fields = "__all__"


class ShirkaSerializer(ModelSerializer):
    class Meta:
        model = Shirka
        fields = "__all__"


class UmrahVisaPriceSerializer(ModelSerializer):
    class Meta:
        model = UmrahVisaPrice
        fields = "__all__"


class UmrahVisaPriceTwoHotelSerializer(ModelSerializer):
    hotel_name = serializers.CharField(
        source="hotel.name", read_only=True
    )  # optional: include hotel name

    class Meta:
        model = UmrahVisaPriceTwoHotel
        exclude = ["umrah_visa_price"]


class UmrahVisaPriceTwoSerializer(serializers.ModelSerializer):
    hotel_details = UmrahVisaPriceTwoHotelSerializer(many=True, required=False)
    vehicle_types = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=VehicleType.objects.all(),
        required=False
    )
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = UmrahVisaPriceTwo
        fields = "__all__"

    def create(self, validated_data):
        hotel_data = validated_data.pop("hotel_details", [])
        vehicle_types = validated_data.pop("vehicle_types", [])

        # create main record
        visa_price = UmrahVisaPriceTwo.objects.create(**validated_data)

        # create related hotel_details
        for hotel in hotel_data:
            UmrahVisaPriceTwoHotel.objects.create(umrah_visa_price=visa_price, **hotel)

        # set ManyToMany vehicle_types
        if vehicle_types:
            visa_price.vehicle_types.set(vehicle_types)

        return visa_price

    def update(self, instance, validated_data):
        hotel_data = validated_data.pop("hotel_details", None)
        vehicle_types = validated_data.pop("vehicle_types", None)

        # update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # reset & recreate hotel_details if provided
        if hotel_data is not None:
            instance.hotel_details.all().delete()
            for hotel in hotel_data:
                UmrahVisaPriceTwoHotel.objects.create(
                    umrah_visa_price=instance, **hotel
                )

        # update vehicle_types if provided
        if vehicle_types is not None:
            instance.vehicle_types.set(vehicle_types)

        return instance



# class OnlyVisaPriceSerializer(ModelSerializer):
#     class Meta:
#         model = OnlyVisaPrice
#         fields = "__all__"
# serializers.py


class TransportSectorPriceSerializer(ModelSerializer):
    class Meta:
        model = TransportSectorPrice
        fields = "__all__"


class AirlinesSerializer(ModelSerializer):
    class Meta:
        model = Airlines
        fields = "__all__"


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class OnlyVisaPriceSerializer(serializers.ModelSerializer):
    # nested city data read-only
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True
    )

    class Meta:
        model = OnlyVisaPrice
        fields = [
            "id",
            "organization",
            "adault_price", "child_price", "infant_price",
            "type", "min_days", "max_days",
            "city", "city_id",
            "status"
        ]

class FoodPriceSerializer(ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        source="city",
        write_only=True,
        required=False,
        allow_null=True
    )
    class Meta:
        model = FoodPrice
        fields = "__all__"


class ZiaratPriceSerializer(ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        source="city",
        write_only=True,
        required=False,
        allow_null=True
    )
    class Meta:
        model = ZiaratPrice
        fields = "__all__"


class BookingExpirySerializer(ModelSerializer):
    class Meta:
        model = BookingExpiry
        fields = "__all__"


class UmrahPackageHotelDetailsSerializer(ModelSerializer):
    hotel_info = HotelsSerializer(source="hotel", read_only=True, required=False)

    class Meta:
        model = UmrahPackageHotelDetails
        exclude = ["package"]


class UmrahPackageTransportDetailsSerializer(ModelSerializer):
    transport_sector_info = TransportSectorPriceSerializer(
        source="transport_sector", read_only=True, required=False
    )

    class Meta:
        model = UmrahPackageTransportDetails
        exclude = ["package"]


class UmrahPackageTicketDetailsSerializer(ModelSerializer):
    ticket_info = TicketSerializer(source="ticket", read_only=True, required=False)

    class Meta:
        model = UmrahPackageTicketDetails
        exclude = ["package"]


class UmrahPackageDiscountDetailsSerializer(ModelSerializer):
    class Meta:
        model = UmrahPackageDiscountDetails
        exclude = ["package"]


class UmrahPackageSerializer(ModelSerializer):
    hotel_details = UmrahPackageHotelDetailsSerializer(many=True, required=False)
    transport_details = UmrahPackageTransportDetailsSerializer(
        many=True, required=False
    )
    ticket_details = UmrahPackageTicketDetailsSerializer(many=True, required=False)
    discount_details = UmrahPackageDiscountDetailsSerializer(many=True, required=False)
    excluded_tickets = serializers.SerializerMethodField(read_only=True)
    adult_price = serializers.SerializerMethodField(read_only=True)
    infant_price = serializers.SerializerMethodField(read_only=True)
    child_discount = serializers.SerializerMethodField(read_only=True)
    quint_room_price = serializers.SerializerMethodField(read_only=True)
    quad_room_price = serializers.SerializerMethodField(read_only=True)
    triple_room_price = serializers.SerializerMethodField(read_only=True)
    double_room_price = serializers.SerializerMethodField(read_only=True)
    sharing_bed_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UmrahPackage
        fields = "__all__"

    def create(self, validated_data):
        hotel_data = validated_data.pop("hotel_details", [])
        transport_data = validated_data.pop("transport_details", [])
        ticket_data = validated_data.pop("ticket_details", [])
        discount_data = validated_data.pop("discount_details", [])

        package = UmrahPackage.objects.create(**validated_data)

        for hotel in hotel_data:
            UmrahPackageHotelDetails.objects.create(package=package, **hotel)

        for transport in transport_data:
            UmrahPackageTransportDetails.objects.create(package=package, **transport)

        for ticket in ticket_data:
            UmrahPackageTicketDetails.objects.create(package=package, **ticket)
        for discount in discount_data:
            UmrahPackageDiscountDetails.objects.create(package=package, **discount)

        return package

    def update(self, instance, validated_data):
        hotel_data = validated_data.pop("hotel_details", [])
        transport_data = validated_data.pop("transport_details", [])
        ticket_data = validated_data.pop("ticket_details", [])
        discount_data = validated_data.pop("discount_details", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Clear old nested data
        instance.hotel_details.all().delete()
        instance.transport_details.all().delete()
        instance.ticket_details.all().delete()
        instance.discount_details.all().delete()

        # Recreate new nested data
        for hotel in hotel_data:
            UmrahPackageHotelDetails.objects.create(package=instance, **hotel)

        for transport in transport_data:
            UmrahPackageTransportDetails.objects.create(package=instance, **transport)

        for ticket in ticket_data:
            UmrahPackageTicketDetails.objects.create(package=instance, **ticket)

        for discount in discount_data:
            UmrahPackageDiscountDetails.objects.create(package=instance, **discount)

        return instance

    def get_excluded_tickets(self, obj):
        """Return full Ticket objects where any of the seat-related fields equals 2147483647
        and the ticket is not part of this package's included ticket_details.
        """
        from tickets.models import Ticket

        MAX_SENTINEL = 2147483647
        included_ids = list(obj.ticket_details.values_list("ticket_id", flat=True))

        qs = Ticket.objects.filter(
            (
                models.Q(total_seats=MAX_SENTINEL)
                | models.Q(left_seats=MAX_SENTINEL)
                | models.Q(booked_tickets=MAX_SENTINEL)
                | models.Q(confirmed_tickets=MAX_SENTINEL)
            )
        ).exclude(id__in=included_ids)

        return TicketSerializer(qs, many=True).data


class PublicUmrahPackageHotelSummarySerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)

    class Meta:
        model = UmrahPackageHotelDetails
        fields = ["hotel_name", "check_in_date", "check_out_date", "number_of_nights"]


class PublicUmrahPackageListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    hotels = PublicUmrahPackageHotelSummarySerializer(source="hotel_details", many=True, read_only=True)

    class Meta:
        model = UmrahPackage
        fields = [
            "id",
            "title",
            "price",
            "total_seats",
            "left_seats",
            "booked_seats",
            "confirmed_seats",
            "available_start_date",
            "available_end_date",
            "reselling_allowed",
            "is_public",
            "hotels",
        ]

    def get_price(self, obj):
        # prefer explicit price_per_person, fallback to adult visa price + service charge
        if getattr(obj, "price_per_person", None):
            return obj.price_per_person
        # try adult price fields
        try:
            return obj.adault_visa_price + (obj.adault_service_charge or 0)
        except Exception:
            return None


class PublicUmrahPackageDetailSerializer(ModelSerializer):
    hotels = PublicUmrahPackageHotelSummarySerializer(source="hotel_details", many=True, read_only=True)
    transport = UmrahPackageTransportDetailsSerializer(source="transport_details", many=True, read_only=True)
    tickets = UmrahPackageTicketDetailsSerializer(source="ticket_details", many=True, read_only=True)

    class Meta:
        model = UmrahPackage
        fields = [
            "id",
            "title",
            "rules",
            "price",
            "price_per_person",
            "adault_visa_price",
            "child_visa_price",
            "infant_visa_price",
            "total_seats",
            "left_seats",
            "booked_seats",
            "confirmed_seats",
            "available_start_date",
            "available_end_date",
            "reselling_allowed",
            "is_public",
            "hotels",
            "transport",
            "tickets",
        ]

    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        if getattr(obj, "price_per_person", None):
            return obj.price_per_person
        try:
            return obj.adault_visa_price + (obj.adault_service_charge or 0)
        except Exception:
            return None

    def get_adult_price(self, obj):
        # keep the original (typo'd) field name as the source
        return getattr(obj, "adault_visa_price", None)

    def get_infant_price(self, obj):
        # infant_price = infant_visa_price + ticket price (use first included ticket if present)
        base = getattr(obj, "infant_visa_price", 0) or 0
        first_ticket = obj.ticket_details.first()
        ticket_price = 0
        if first_ticket and getattr(first_ticket, "ticket", None):
            ticket_obj = first_ticket.ticket
            ticket_price = getattr(ticket_obj, "adult_price", 0) or 0
        return base + ticket_price

    def get_child_discount(self, obj):
        # use child_visa_price as the flat child discount/price if present
        return getattr(obj, "child_visa_price", None)

    def _first_hotel_field(self, obj, field_name):
        first = obj.hotel_details.first()
        if not first:
            return None
        return getattr(first, field_name, None)

    def get_quint_room_price(self, obj):
        return self._first_hotel_field(obj, "quaint_bed_price")

    def get_quad_room_price(self, obj):
        return self._first_hotel_field(obj, "quad_bed_price")

    def get_triple_room_price(self, obj):
        return self._first_hotel_field(obj, "triple_bed_price")

    def get_double_room_price(self, obj):
        return self._first_hotel_field(obj, "double_bed_price")

    def get_sharing_bed_price(self, obj):
        return self._first_hotel_field(obj, "sharing_bed_price")


class CustomUmrahPackageHotelDetailsSerializer(ModelSerializer):
    hotel_info = HotelsSerializer(source="hotel", read_only=True, required=False)

    class Meta:
        model = CustomUmrahPackageHotelDetails
        exclude = ["package"]


class CustomUmrahPackageTransportDetailsSerializer(ModelSerializer):
    transport_sector_info = TransportSectorPriceSerializer(
        source="transport_sector", read_only=True, required=False
    )

    class Meta:
        model = CustomUmrahPackageTransportDetails
        exclude = ["package"]


class CustomUmrahPackageTicketDetailsSerializer(ModelSerializer):
    ticket_info = TicketSerializer(source="ticket", read_only=True, required=False)

    class Meta:
        model = CustomUmrahPackageTicketDetails
        exclude = ["package"]


class CustomUmrahZiaratDetailsSerializer(ModelSerializer):
    class Meta:
        model = CustomUmrahZiaratDetails
        exclude = ["package"]


class CustomUmrahFoodDetailsSerializer(ModelSerializer):
    class Meta:
        model = CustomUmrahFoodDetails
        exclude = ["package"]


class CustomUmrahPackageSerializer(ModelSerializer):
    # agent_name = serializers.CharField(source="agent.username", read_only=True)
    agency_name = serializers.CharField(source="agency.name", read_only=True)
    hotel_details = CustomUmrahPackageHotelDetailsSerializer(many=True, required=False)
    transport_details = CustomUmrahPackageTransportDetailsSerializer(
        many=True, required=False
    )
    ticket_details = CustomUmrahPackageTicketDetailsSerializer(
        many=True, required=False
    )
    ziarat_details = CustomUmrahZiaratDetailsSerializer(many=True, required=False)
    food_details = CustomUmrahFoodDetailsSerializer(many=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = CustomUmrahPackage
        fields = "__all__"

    def create(self, validated_data):
        hotel_data = validated_data.pop("hotel_details", [])
        transport_data = validated_data.pop("transport_details", [])
        ticket_data = validated_data.pop("ticket_details", [])
        ziarat_data = validated_data.pop("ziarat_details", [])
        food_data = validated_data.pop("food_details", [])

        package = CustomUmrahPackage.objects.create(**validated_data)

        for hotel in hotel_data:
            CustomUmrahPackageHotelDetails.objects.create(package=package, **hotel)

        for transport in transport_data:
            CustomUmrahPackageTransportDetails.objects.create(
                package=package, **transport
            )

        for ticket in ticket_data:
            CustomUmrahPackageTicketDetails.objects.create(package=package, **ticket)
        for ziarat in ziarat_data:
            CustomUmrahZiaratDetails.objects.create(package=package, **ziarat)
        for food in food_data:
            CustomUmrahFoodDetails.objects.create(package=package, **food)

        return package

    def update(self, instance, validated_data):
        hotel_data = validated_data.pop("hotel_details", None)
        transport_data = validated_data.pop("transport_details", None)
        ticket_data = validated_data.pop("ticket_details", None)
        ziarat_data = validated_data.pop("ziarat_details", None)
        food_data = validated_data.pop("food_details", None)

        # Update scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Conditionally update nested relations
        if hotel_data is not None:
            instance.hotel_details.all().delete()
            for hotel in hotel_data:
                CustomUmrahPackageHotelDetails.objects.create(package=instance, **hotel)

        if transport_data is not None:
            instance.transport_details.all().delete()
            for transport in transport_data:
                CustomUmrahPackageTransportDetails.objects.create(
                    package=instance, **transport
                )

        if ticket_data is not None:
            instance.ticket_details.all().delete()
            for ticket in ticket_data:
                CustomUmrahPackageTicketDetails.objects.create(
                    package=instance, **ticket
                )

        if ziarat_data is not None:
            instance.ziarat_details.all().delete()
            for ziarat in ziarat_data:
                CustomUmrahZiaratDetails.objects.create(package=instance, **ziarat)

        if food_data is not None:
            instance.food_details.all().delete()
            for food in food_data:
                CustomUmrahFoodDetails.objects.create(package=instance, **food)

        return instance


class SetVisaTypeSerializer(ModelSerializer):
    class Meta:
        model = SetVisaType
        fields = "__all__"

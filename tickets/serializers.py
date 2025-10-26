from rest_framework import serializers
from .models import (
    Ticket,
    TicketTripDetails,
    TickerStopoverDetails,
    HotelPrices,
    HotelContactDetails,
    Hotels,
    HotelRooms,
    RoomDetails,
)


class TickerStopoverDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickerStopoverDetails
        fields = "__all__"
        extra_kwargs = {"ticket": {"required": False}}


class TicketTripDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTripDetails
        fields = "__all__"
        extra_kwargs = {"ticket": {"required": False}}


class TicketSerializer(serializers.ModelSerializer):
    trip_details = TicketTripDetailsSerializer(many=True)
    stopover_details = TickerStopoverDetailsSerializer(many=True, required=False)

    class Meta:
        model = Ticket
        fields = "__all__"

    def create(self, validated_data):
        trip_details_data = validated_data.pop("trip_details", [])
        stopover_details_data = validated_data.pop("stopover_details", [])

        ticket = Ticket.objects.create(**validated_data)

        # Create trip details
        for trip in trip_details_data:
            TicketTripDetails.objects.create(ticket=ticket, **trip)

        # Create stopover details
        for stopover in stopover_details_data:
            TickerStopoverDetails.objects.create(ticket=ticket, **stopover)

        return ticket

    def update(self, instance, validated_data):
        trip_details_data = validated_data.pop("trip_details", None)
        stopover_details_data = validated_data.pop("stopover_details", None)

        # Update base Ticket fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update trip details only if provided
        if trip_details_data is not None:
            instance.trip_details.all().delete()
            for trip in trip_details_data:
                TicketTripDetails.objects.create(ticket=instance, **trip)

        # Update stopover details only if provided
        if stopover_details_data is not None:
            instance.stopover_details.all().delete()
            for stopover in stopover_details_data:
                TickerStopoverDetails.objects.create(ticket=instance, **stopover)

        return instance


class HotelPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPrices
        exclude = ["hotel"]


class HotelContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelContactDetails
        exclude = ["hotel"]


class HotelsSerializer(serializers.ModelSerializer):
    prices = HotelPricesSerializer(many=True)
    contact_details = HotelContactDetailsSerializer(many=True, required=False)

    class Meta:
        model = Hotels
        fields = "__all__"

    def create(self, validated_data):
        prices_data = validated_data.pop("prices", [])
        contact_details_data = validated_data.pop("contact_details", [])
        hotel = Hotels.objects.create(**validated_data)

        for price in prices_data:
            HotelPrices.objects.create(hotel=hotel, **price)
        for contact in contact_details_data:
            HotelContactDetails.objects.create(hotel=hotel, **contact)
        return hotel

    def update(self, instance, validated_data):
        prices_data = validated_data.pop("prices", None)
        contact_details_data = validated_data.pop("contact_details", None)

        # Update main Hotel fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update prices only if provided
        if prices_data is not None:
            instance.prices.all().delete()
            for price in prices_data:
                HotelPrices.objects.create(hotel=instance, **price)
        if contact_details_data is not None:
            instance.contact_details.all().delete()
            for contact in contact_details_data:
                HotelContactDetails.objects.create(hotel=instance, **contact)
        return instance


class HotelRoomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDetails
        exclude = ["room"]


class HotelRoomsSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    details = HotelRoomDetailsSerializer(many=True, required=False)

    class Meta:
        model = HotelRooms
        fields = "__all__"

    def create(self, validated_data):
        details_data = validated_data.pop("details", [])
        room = HotelRooms.objects.create(**validated_data)

        for detail in details_data:
            RoomDetails.objects.create(room=room, **detail)
        return room

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        # Update main HotelRoom fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update details only if provided
        if details_data is not None:
            instance.details.all().delete()
            for detail in details_data:
                RoomDetails.objects.create(room=instance, **detail)
        return instance

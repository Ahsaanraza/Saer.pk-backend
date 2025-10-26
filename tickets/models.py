from django.db import models
from organization.models import Organization
from packages.models import Airlines, City
from django.contrib.auth.models import User

# Create your models here.


class Ticket(models.Model):
    """
    Model to store the details of a Ticket.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="tickets"
    )
    airline = models.ForeignKey(
        Airlines, on_delete=models.CASCADE, related_name="tickets"
    )
    is_meal_included = models.BooleanField(default=False)
    is_refundable = models.BooleanField(default=False)
    pnr = models.CharField(max_length=100)
    child_price = models.FloatField(default=0)
    infant_price = models.FloatField(default=0)
    adult_price = models.FloatField(default=0)
    total_seats = models.IntegerField(default=0)
    left_seats = models.IntegerField(default=0)
    booked_tickets = models.IntegerField(default=0)
    confirmed_tickets = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    pieces = models.IntegerField(default=0)
    is_umrah_seat = models.BooleanField(default=False)
    trip_type = models.CharField(max_length=50)
    departure_stay_type = models.CharField(max_length=50)
    return_stay_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, blank=True, null=True)
    inventory_owner_organization_id = models.IntegerField(blank=True, null=True)



class TicketTripDetails(models.Model):
    """
    Model to store the trip details of a Ticket.
    """

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="trip_details"
    )
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    departure_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="departure_tickets"
    )
    arrival_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="arrival_tickets"
    )
    trip_type = models.CharField(max_length=50)


class TickerStopoverDetails(models.Model):
    """
    Model to store the stopover details of a Ticket.
    """

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="stopover_details"
    )
    stopover_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="stopover_tickets"
    )
    stopover_duration = models.CharField(max_length=100)
    trip_type = models.CharField(max_length=50)


class Hotels(models.Model):
    """
    Model to store the details of a Hotel.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="hotels"
    )
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="hotels")
    address = models.TextField()
    google_location = models.CharField(max_length=255, blank=True, null=True)
    google_drive_link = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=50)
    distance = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    available_start_date = models.DateField()
    available_end_date = models.DateField()
    status = models.CharField(max_length=50, blank=True, null=True)


class HotelPrices(models.Model):
    """
    Model to store the prices of a Hotel.
    """

    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name="prices")
    start_date = models.DateField()
    end_date = models.DateField()
    room_type = models.CharField(max_length=50)
    price= models.FloatField(default=0)
    is_sharing_allowed = models.BooleanField(default=False)
    # room_price = models.FloatField(default=0)
    # quint_price = models.FloatField(default=0)
    # quad_price = models.FloatField(default=0)
    # triple_price = models.FloatField(default=0)
    # double_price = models.FloatField(default=0)


class HotelContactDetails(models.Model):
    """
    Model to store the contact details of a Hotel.
    """

    hotel = models.ForeignKey(
        Hotels, on_delete=models.CASCADE, related_name="contact_details"
    )
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)


class HotelRooms(models.Model):
    """
    Model to store the details of a Hotel Room.
    """

    hotel = models.ForeignKey(Hotels, on_delete=models.PROTECT, related_name="rooms")
    floor = models.CharField(max_length=50)
    room_type = models.CharField(max_length=50)
    room_number = models.CharField(max_length=20)
    total_beds = models.IntegerField(default=1)

class RoomDetails(models.Model):
    """
    Model to store the details of a Hotel Room.
    """

    room = models.ForeignKey(HotelRooms, on_delete=models.CASCADE, related_name="details")
    bed_number = models.CharField(max_length=20)
    is_assigned = models.BooleanField(default=False)
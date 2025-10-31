
from django.db import models
import hmac
import hashlib
import secrets
from django.conf import settings
from django.contrib.auth.models import User
from organization.models import Organization, Branch, Agency
from packages.models import TransportSectorPrice, City, Shirka

# BookingCallRemark model for call remarks on bookings
class BookingCallRemark(models.Model):
    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE, related_name='call_remarks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remark_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization, Branch, Agency
from packages.models import TransportSectorPrice, City, Shirka


# ...existing code...

# Place BookingCallRemark model after all imports and before other model classes

class BookingCallRemark(models.Model):
    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE, related_name='call_remarks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remark_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.


class Bank(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    account_title = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.TextField(blank=True, null=True)
    iban = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.branch_code}"
class InternalNote(models.Model):
    NOTE_STATUS = (
        ("clear", "Clear"),
        ("not_clear", "Not Clear"),
    )

    note_type = models.CharField(max_length=255)
    follow_up_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="internal_notes")  
    date_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    note = models.TextField()
    attachment = models.FileField(upload_to="internal_notes/", null=True, blank=True)
    working_status = models.CharField(max_length=20, choices=NOTE_STATUS, default="not_clear")

    def __str__(self):
        return f"{self.note_type} - {self.employee.username}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    rejected_employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rejected_employer", blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="bookings"
    )
    internals = models.ManyToManyField(
        InternalNote, related_name="bookings", blank=True, null=True
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="bookings"
    )
    agency = models.ForeignKey(
        Agency, on_delete=models.CASCADE, related_name="bookings"
    )
    confirmed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="confirmed_bookings", blank=True, null=True
    )
    selling_organization_id = models.IntegerField(blank=True, null=True)
    owner_organization_id = models.IntegerField(blank=True, null=True)
    booking_number = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    expiry_time= models.DateTimeField(blank=True, null=True)
    total_pax = models.IntegerField(default=0)
    total_adult = models.IntegerField(default=0)
    total_infant = models.IntegerField(default=0)
    total_child = models.IntegerField(default=0)
    total_ticket_amount = models.FloatField(default=0)
    total_hotel_amount = models.FloatField(default=0)
    total_transport_amount = models.FloatField(default=0)
    total_visa_amount = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    
    total_hotel_amount_pkr = models.FloatField(default=0, blank=True, null=True)
    total_hotel_amount_sar = models.FloatField(default=0, blank=True, null=True)

    total_ziyarat_amount_pkr = models.FloatField(default=0, blank=True, null=True)
    total_ziyarat_amount_sar = models.FloatField(default=0, blank=True, null=True)

    total_food_amount_pkr = models.FloatField(default=0, blank=True, null=True)
    total_food_amount_sar = models.FloatField(default=0, blank=True, null=True)

    total_transport_amount_pkr = models.FloatField(default=0, blank=True, null=True)
    total_transport_amount_sar = models.FloatField(default=0, blank=True, null=True)

    total_visa_amount_pkr = models.FloatField(default=0, blank=True, null=True)
    total_visa_amount_sar = models.FloatField(default=0, blank=True, null=True)

    total_ticket_amount_pkr = models.FloatField(default=0, blank=True, null=True)

    total_in_pkr = models.FloatField(default=0, blank=True, null=True)

    paid_payment = models.FloatField(default=0, blank=True, null=True)
    pending_payment = models.FloatField(default=0, blank=True, null=True)

    umrah_package = models.ForeignKey(
        "packages.UmrahPackage", on_delete=models.SET_NULL, blank=True, null=True, related_name="bookings"
    )

    call_status = models.BooleanField(default=False) 
    client_note = models.TextField(blank=True, null=True)  
    
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20, default="Pending")
    is_partial_payment_allowed = models.BooleanField(default=False)
    category = models.CharField(max_length=20,blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    action = models.CharField(max_length=100, blank=True, null=True) 
    rejected_notes = models.TextField(blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    is_visa_price_pkr = models.BooleanField(default=True)  # True → PKR, False → SAR
    visa_riyal_rate = models.FloatField(default=0, blank=True, null=True)  # Riyal rate at booking time
    visa_rate = models.FloatField(default=0, blank=True, null=True)        # Base visa rate (jis currency me diya gaya)
    visa_rate_in_sar = models.FloatField(default=0, blank=True, null=True) # Converted visa rate in SAR
    visa_rate_in_pkr = models.FloatField(default=0, blank=True, null=True)
    is_ziyarat_included = models.BooleanField(default=False)
    is_food_included = models.BooleanField(default=False)
    inventory_owner_organization_id = models.IntegerField(blank=True, null=True)
    booking_organization_id = models.IntegerField(blank=True, null=True)

    # New fields requested:
    BOOKING_TYPE_CHOICES = [
        ("TICKET", "Ticket"),
        ("UMRAH", "Umrah Package"),
        ("HOTEL", "Hotel"),
        ("OTHER", "Other"),
    ]
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, default="TICKET")
    is_full_package = models.BooleanField(default=False)
    # Public booking flags and metadata
    is_public_booking = models.BooleanField(default=False)
    created_by_user_type = models.CharField(max_length=30, blank=True, null=True)
    # invoice / external booking number (unique public-facing invoice id)
    invoice_no = models.CharField(max_length=64, unique=True, blank=True, null=True)
    # accumulate payments (use decimal for accuracy)
    total_payment_received = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Flag to indicate if any part of booking uses external/outsourced services (hotels)
    is_outsourced = models.BooleanField(default=False)

    # payments: optional JSON array to store payment entries (mirrors Payment model or quick payload)
    payments = models.JSONField(default=list, blank=True)

    # journal_items: list of line items (name, price, qty, total) for bookkeeping
    journal_items = models.JSONField(default=list, blank=True)

    reseller_commission = models.FloatField(default=0, blank=True, null=True)
    markup_by_reseller = models.FloatField(default=0, blank=True, null=True)
    # Public secure reference for read-only public access (QR / hashed link)
    public_ref = models.CharField(max_length=128, unique=True, blank=True, null=True)
    # URL encoded in voucher QR (public-facing). Populated on save if possible.
    voucher_qr_url = models.CharField(max_length=512, blank=True, null=True)

    def generate_public_ref(self):
        """Generate a unique HMAC-SHA256 based public reference using SECRET_KEY and booking_number.

        Format: INV-{booking_number}-{HEX}
        Only first 12 chars of digest are kept for readability.
        Ensures uniqueness by appending a counter if collision occurs (rare).
        """
        # base value uses booking_number if available, else fallback to id/secret
        base = (self.booking_number or str(self.id) or secrets.token_hex(8)).encode()
        key = settings.SECRET_KEY.encode()
        digest = hmac.new(key, base + (str(self.date.timestamp()).encode() if getattr(self, 'date', None) else b""), hashlib.sha256).hexdigest()
        short = digest[:12].upper()
        candidate = f"INV-{self.booking_number}-{short}" if self.booking_number else f"INV-{short}"

        # ensure uniqueness
        from django.db import transaction

        counter = 0
        unique_candidate = candidate
        while True:
            exists = Booking.objects.filter(public_ref=unique_candidate).exists()
            if not exists:
                break
            counter += 1
            unique_candidate = f"{candidate}-{counter}"

        self.public_ref = unique_candidate

    def generate_invoice_no(self):
        """Generate a short unique invoice number for public bookings."""
        import secrets

        if self.invoice_no:
            return
        base = (self.booking_number or str(self.id) or secrets.token_hex(6)).encode()
        short = secrets.token_hex(6).upper()
        candidate = f"INV-{short}"
        counter = 0
        unique_candidate = candidate
        while Booking.objects.filter(invoice_no=unique_candidate).exists():
            counter += 1
            unique_candidate = f"{candidate}-{counter}"
        self.invoice_no = unique_candidate

    def save(self, *args, **kwargs):
        # generate public_ref on first save if missing
        is_new = self.pk is None
        super().save(*args, **kwargs)
        try:
            if not self.public_ref:
                # regenerate now that we have a PK/date
                self.generate_public_ref()
                super().save(update_fields=["public_ref"])
        except Exception:
            # Do not block normal booking saves if public_ref generation fails
            pass

        # populate voucher QR url (if public_ref is present and there's a configured site base)
        try:
            if self.public_ref and (not self.voucher_qr_url):
                from django.conf import settings as _settings
                site_base = getattr(_settings, 'SITE_BASE_URL', None) or getattr(_settings, 'FRONTEND_URL', None) or 'http://localhost:8000'
                url = f"{site_base.rstrip('/')}/order-status/?ref={self.public_ref}"
                # write back quietly
                self.voucher_qr_url = url
                super().save(update_fields=['voucher_qr_url'])
        except Exception:
            # Do not block saving for QR population failures
            pass

class BookingHotelDetails(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="hotel_details"
    )
    hotel = models.ForeignKey("tickets.Hotels", on_delete=models.PROTECT)
    check_in_date = models.DateField(blank=True, null=True)
    check_out_date = models.DateField(blank=True, null=True)
    number_of_nights = models.IntegerField(default=0)
    room_type = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    riyal_rate = models.FloatField(default=0)
    is_price_pkr= models.BooleanField(default=True)
    contact_person_name = models.CharField(max_length=255, blank=True, null=True)
    contact_person_number = models.CharField(max_length=20, blank=True, null=True)
    leg_no = models.PositiveIntegerField(default=1)  
    check_in_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="inactive"
    )
    check_out_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="inactive"
    )
    total_in_riyal_rate = models.FloatField(blank=True, null=True)
    total_in_pkr = models.FloatField(blank=True, null=True)
    hotel_brn = models.CharField(max_length=100, blank=True, null=True)
    hotel_voucher_number = models.CharField(max_length=100, blank=True, null=True)
    special_request = models.TextField(blank=True, null=True)  
    sharing_type = models.CharField(max_length=50, blank=True, null=True)
    self_hotel_name = models.CharField(max_length=255, blank=True, null=True)
    # mark if this particular hotel detail row is from an outsourced/external hotel
    outsourced_hotel = models.BooleanField(default=False)
    def __str__(self):
        # Be defensive: related `hotel` object may be missing (stale FK).
        # Accessing `self.hotel` can raise DoesNotExist during admin rendering
        # if the related Hotels row was deleted. Fall back to hotel_id.
        try:
            hotel = self.hotel
        except Exception:
            hotel = f"[missing hotel id={getattr(self, 'hotel_id', None)}]"
        return f"{self.booking} - {hotel}"


class HotelOutsourcing(models.Model):
    """Record for outsourced/external hotel bookings tied to a Booking.

    Created when a passenger's hotel is sourced externally. This model is soft-deleteable
    via `is_deleted` and holds a pointer to ledger entries created for payables.
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='outsourcing_records')
    booking_hotel_detail = models.ForeignKey(
        BookingHotelDetails, on_delete=models.SET_NULL, null=True, blank=True, related_name='outsourcing'
    )
    hotel_name = models.CharField(max_length=255)
    source_company = models.CharField(max_length=255, blank=True, null=True)
    check_in_date = models.DateField(blank=True, null=True)
    check_out_date = models.DateField(blank=True, null=True)
    room_type = models.CharField(max_length=100, blank=True, null=True)
    room_no = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField(default=0)  # price per night
    quantity = models.PositiveIntegerField(default=1)
    number_of_nights = models.IntegerField(default=1)
    currency = models.CharField(max_length=10, default='PKR')
    remarks = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    agent_notified = models.BooleanField(default=False)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    # link to ledger entry created for this outsourcing (if any)
    ledger_entry_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
        # Prevent duplicate active outsourcing for same booking/hotel detail
        constraints = [
            models.UniqueConstraint(fields=['booking', 'booking_hotel_detail'], condition=models.Q(is_deleted=False), name='unique_active_outsource_per_hoteldetail')
        ]

    @property
    def outsource_cost(self):
        try:
            return float(self.price) * float(self.quantity) * int(self.number_of_nights)
        except Exception:
            return 0.0

    def soft_delete(self):
        self.is_deleted = True
        self.save()


class BookingTransportDetails(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="transport_details"
    )
    # transport_sector = models.ForeignKey(TransportSectorPrice, on_delete=models.PROTECT)
    shirka= models.ForeignKey(Shirka, on_delete=models.PROTECT, blank=True, null=True)
    vehicle_type = models.ForeignKey(
        "VehicleType", on_delete=models.SET_NULL, null=True, blank=True, related_name="transport_details"
    )
    # vehicle_type = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    is_price_pkr= models.BooleanField(default=True)
    riyal_rate = models.FloatField(default=0)
    
    price_in_pkr = models.FloatField(default=0)       
    price_in_sar = models.FloatField(default=0) 
    voucher_no = models.CharField(max_length=100, blank=True, null=True)
    brn_no = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.booking} - {self.vehicle_type.vehicle_name if self.vehicle_type else 'No Vehicle'}"


class BookingTicketDetails(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="ticket_details"
    )
    ticket = models.ForeignKey("tickets.Ticket", on_delete=models.PROTECT)
    is_meal_included = models.BooleanField(default=False)
    is_refundable = models.BooleanField(default=False)
    pnr = models.CharField(max_length=100)
    child_price = models.FloatField(default=0)
    infant_price = models.FloatField(default=0)
    adult_price = models.FloatField(default=0)
    seats = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    pieces = models.IntegerField(default=0)
    is_umrah_seat = models.BooleanField(default=False)
    trip_type = models.CharField(max_length=50)
    departure_stay_type = models.CharField(max_length=50)
    return_stay_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, blank=True, null=True)
    # is_price_pkr= models.BooleanField(default=True)
    # riyal_rate = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        """
        Override save to update Ticket counters (booked_tickets, confirmed_tickets, left_seats)
        when booking ticket details are created or updated.
        """
        from tickets.models import Ticket

        old = None
        if self.pk:
            try:
                old = BookingTicketDetails.objects.get(pk=self.pk)
            except BookingTicketDetails.DoesNotExist:
                old = None

        super().save(*args, **kwargs)

        try:
            ticket = Ticket.objects.get(pk=self.ticket_id)
        except Ticket.DoesNotExist:
            return

        # compute seat delta for booked_tickets
        new_seats = self.seats or 0
        old_seats = old.seats if old else 0
        delta = new_seats - old_seats

        if delta != 0:
            ticket.booked_tickets = max(0, ticket.booked_tickets + delta)
            ticket.left_seats = max(0, ticket.total_seats - ticket.booked_tickets)

        # handle confirmed status transition
        old_status = getattr(old, 'status', None)
        new_status = self.status
        if old_status != 'Confirmed' and new_status == 'Confirmed':
            # add to confirmed_tickets
            ticket.confirmed_tickets = ticket.confirmed_tickets + new_seats
        elif old_status == 'Confirmed' and new_status != 'Confirmed':
            # remove from confirmed_tickets
            ticket.confirmed_tickets = max(0, ticket.confirmed_tickets - old_seats)

        ticket.save()

    def delete(self, *args, **kwargs):
        """Adjust ticket counters when booking ticket detail is deleted."""
        from tickets.models import Ticket

        try:
            ticket = Ticket.objects.get(pk=self.ticket_id)
        except Ticket.DoesNotExist:
            super().delete(*args, **kwargs)
            return

        # subtract seats
        seats = self.seats or 0
        ticket.booked_tickets = max(0, ticket.booked_tickets - seats)
        ticket.left_seats = max(0, ticket.total_seats - ticket.booked_tickets)

        if self.status == 'Confirmed':
            ticket.confirmed_tickets = max(0, ticket.confirmed_tickets - seats)

        ticket.save()
        super().delete(*args, **kwargs)


class BookingTicketTicketTripDetails(models.Model):
    ticket = models.ForeignKey(
        BookingTicketDetails, on_delete=models.CASCADE, related_name="trip_details"
    )
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    departure_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="booking_departure_city"
    )
    arrival_city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="booking_arrival_city"
    )
    trip_type = models.CharField(max_length=50)


class BookingTicketStopoverDetails(models.Model):
    ticket = models.ForeignKey(
        BookingTicketDetails, on_delete=models.CASCADE, related_name="stopover_details"
    )
    stopover_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
    )
    stopover_duration = models.CharField(max_length=100)
    trip_type = models.CharField(max_length=50)


class BookingPersonDetail(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="person_details"
    )
    age_group = models.CharField(max_length=20, blank=True, null=True)
    person_title = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    passpoet_issue_date = models.DateField(blank=True, null=True)
    passport_expiry_date = models.DateField(blank=True, null=True)
    passport_picture = models.ImageField(
        upload_to="media/passport_pictures", blank=True, null=True
    )
    country = models.CharField(max_length=50, blank=True, null=True)
    is_visa_included = models.BooleanField(default=False)
    visa_price = models.FloatField(default=0)
    is_family_head = models.BooleanField(default=False)
    family_number= models.IntegerField(default=0)
    shirka = models.ForeignKey(Shirka, on_delete=models.PROTECT, blank=True, null=True)
    visa_status = models.CharField(
        max_length=20, default="Pending"
    )  # e.g., Pending, Approved, Rejected
    ticket_status = models.CharField(
        max_length=20, default="Pending"
    )  # e.g., Pending, Confirmed, Cancelled
    ticket_remarks = models.TextField(blank=True, null=True)
    visa_group_number = models.CharField(max_length=20, blank=True, null=True)
    visa_remarks = models.TextField(blank=True, null=True)  # visa remarks
    contact_number = models.CharField(max_length=20, blank=True, null=True)  # contact number
    this_pex_remarks = models.TextField(blank=True, null=True)  # this pex remarks
    ticket_price = models.FloatField(default=0)  # ticket price
    ticket_discount = models.FloatField(default=0)
    is_visa_price_pkr = models.BooleanField(default=True)  # True → PKR, False → SAR
    visa_riyal_rate = models.FloatField(default=0, blank=True, null=True)  # Riyal rate at booking
    visa_rate = models.FloatField(default=0, blank=True, null=True)        # Base visa rate
    visa_rate_in_sar = models.FloatField(default=0, blank=True, null=True) # Converted to SAR
    visa_rate_in_pkr = models.FloatField(default=0, blank=True, null=True) # Converted to PKR
    ticket_included = models.BooleanField(default=True)
    # ticket_voucher_number = models.CharField(max_length=20, blank=True, null=True)
    # ticker_brn= models.CharField(max_length=20, blank=True, null=True)
    # food_voucher_number = models.CharField(max_length=20, blank=True, null=True)
    # food_brn = models.CharField(max_length=20, blank=True, null=True)
    # ziyarat_voucher_number = models.CharField(max_length=20, blank=True, null=True)
    # ziyarat_brn = models.CharField(max_length=20, blank=True, null=True)
    # transport_voucher_number = models.CharField(max_length=20, blank=True, null=True)
    # transport_brn = models.CharField(max_length=20, blank=True, null=True)

class BookingPersonContactDetails(models.Model):
    person = models.ForeignKey(
        BookingPersonDetail, on_delete=models.CASCADE, related_name="contact_details"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

class BookingPersonZiyaratDetails(models.Model):
    person = models.ForeignKey(
        BookingPersonDetail, on_delete=models.CASCADE, related_name="ziyarat_details"
    )
    city = models.CharField(max_length=50) 
    total_pax = models.IntegerField(default=0)  
    per_pax_price = models.FloatField(default=0)  
    total_price = models.FloatField(default=0)  
    total_price_in_pkr = models.FloatField(default=0)  
    price_in_sar = models.FloatField(default=0) 
    date= models.DateField()
    price = models.FloatField(default=0)
    is_price_pkr= models.BooleanField(default=True)
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)  
    contact_number = models.CharField(max_length=20, blank=True, null=True)  

    ziyarar_voucher_number = models.CharField(max_length=100, blank=True, null=True)  
    ziyarat_brn = models.CharField(max_length=100, blank=True, null=True)  

    is_price_pkr = models.BooleanField(default=True)  
    riyal_rate = models.FloatField(default=0)


class BookingPersonFoodDetails(models.Model):
    person = models.ForeignKey(
        BookingPersonDetail, on_delete=models.CASCADE, related_name="food_details"
    )
    food = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    is_price_pkr= models.BooleanField(default=True)
    total_pax = models.IntegerField(default=0)  
    per_pax_price = models.FloatField(default=0)  
    total_price = models.FloatField(default=0)  
    total_price_in_pkr = models.FloatField(default=0)  
    price_in_sar = models.FloatField(default=0)  

    contact_person_name = models.CharField(max_length=100, blank=True, null=True)  
    contact_number = models.CharField(max_length=20, blank=True, null=True)  

    food_voucher_number = models.CharField(max_length=100, blank=True, null=True)  
    food_brn = models.CharField(max_length=100, blank=True, null=True)  

    riyal_rate = models.FloatField(default=0)


class Payment(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="payments"
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="payments"
    )
    agency = models.ForeignKey(
        Agency, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    agent = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_payments",
        blank=True,
        null=True,
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment_details",
        blank=True,
        null=True,
    )
    method = models.CharField(max_length=50)
    bank = models.ForeignKey(
        Bank, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    # Agent bank (optional) - bank used by the agent for this payment
    agent_bank = models.ForeignKey(
        Bank, on_delete=models.SET_NULL, related_name="agent_payments", blank=True, null=True
    )
    # Organization bank (optional) - bank account of the organization receiving the payment
    organization_bank = models.ForeignKey(
        Bank, on_delete=models.SET_NULL, related_name="organization_payments", blank=True, null=True
    )
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, default="Pending"
    )  # e.g., Pending, Completed, Failed
    image = models.ImageField(upload_to="media/payment_receipts", blank=True, null=True)
    transaction_number = models.CharField(max_length=100, blank=True, null=True)
    # KuickPay transaction/reference number (optional)
    kuickpay_trn = models.CharField(max_length=128, blank=True, null=True)
    # Public-mode flag indicates this payment was created by an unauthenticated/public flow
    public_mode = models.BooleanField(default=False)
class Sector(models.Model):
    departure_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="departure_sectors",
        null=True,
        blank=True
    )
    arrival_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="arrival_sectors",
        null=True,
        blank=True
    )
    contact_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="sectors"
    )
    class Meta:
        db_table = "small_sector"

    def __str__(self):
        return f"{self.departure_city or '---'} → {self.arrival_city or '---'}"
class BigSector(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="big_sectors"
    )
    small_sectors = models.ManyToManyField(Sector, related_name="big_sectors")

    class Meta:
        db_table = "big_sector"

    def __str__(self):
        return f"BigSector #{self.id} ({self.organization.name})"

class VehicleType(models.Model):
    vehicle_name = models.CharField(max_length=100)  
    small_sector = models.ForeignKey(
        Sector, on_delete=models.SET_NULL, related_name="vehicle_types", null=True, blank=True
    )
    big_sector = models.ForeignKey(
        BigSector, on_delete=models.SET_NULL, related_name="vehicle_types", null=True, blank=True
    )
    vehicle_type = models.CharField(max_length=100)  # simple varchar
    price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(null=True, blank=True)
    visa_type = models.CharField(max_length=100)  
    status = models.CharField(max_length=10, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="vehicle_types"
    )

    class Meta:
        db_table = "vehicle_type"

    def __str__(self):
        return self.vehicle_name
        
class BookingTransportSector(models.Model):
    transport_detail = models.ForeignKey(
        BookingTransportDetails, on_delete=models.CASCADE, related_name="sector_details"
    )
    sector_no = models.IntegerField(default=0)  # SECTOR NO
    small_sector_id = models.IntegerField(blank=True, null=True)  # SMALL SECTOR ID (ya FK banani ho to bata dena)
    date = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)
    voucher_no = models.CharField(max_length=100, blank=True, null=True)
    brn_no = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Sector {self.sector_no} - {self.transport_detail_id}"
class BankAccount(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    bank_name = models.CharField(max_length=255)
    account_title = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    iban = models.CharField(max_length=34, unique=True)

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="bank_accounts",blank=True, null=True
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="bank_accounts",blank=True, null=True
    )
    agency = models.ForeignKey(
        Agency, on_delete=models.CASCADE, related_name="bank_accounts",blank=True, null=True
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_title}"
class OrganizationLink(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]

    organization_id = models.IntegerField()  # ya ForeignKey to Organization agar table hai
    this_organization_request = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    main_organization_request = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    request_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Org {self.organization_id} ({self.this_organization_request}/{self.main_organization_request})"
class AllowedReseller(models.Model):
    inventory_owner_company = models.ForeignKey(
        OrganizationLink, on_delete=models.CASCADE, related_name="allowed_resellers"
    )

    # Single reseller company allowed to resell the owner's inventory
    reseller_company = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="reseller_links",
        null=True, blank=True
    )

    ALLOWED_CHOICES = [
        ("GROUP_TICKETS", "Group Tickets"),
        ("UMRAH_PACKAGES", "Umrah Packages"),
        ("HOTELS", "Hotels"),
    ]

    # Which inventory types the reseller is allowed to access. Stored as JSON list.
    allowed_types = models.JSONField(default=list)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]
    requested_status_by_reseller = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )

    # Link to discount group (optional)
    discount_group = models.ForeignKey(
        "DiscountGroup", on_delete=models.SET_NULL, null=True, blank=True, related_name="allowed_resellers"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.inventory_owner_company} → Resellers"
class DiscountGroup(models.Model):
    name = models.CharField(max_length=255)
    # optional group_type to classify discount groups (e.g., "SENIOR", "STUDENT", "CORPORATE")
    group_type = models.CharField(max_length=100, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="discount_groups")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class Discount(models.Model):
    discount_group = models.ForeignKey(DiscountGroup, on_delete=models.CASCADE, related_name="discounts")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="discounts")

    # kis cheez pe discount hai
    things = models.CharField(
        max_length=50,
        choices=[
            ("group_ticket", "Group Ticket"),
            ("umrah_package", "Umrah Package"),
            ("hotel", "Hotel"),
        ]
    )

    # ticket / package discount
    group_ticket_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    umrah_package_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, choices=[("PKR", "PKR"), ("SAR", "SAR")], default="PKR")

    # hotel discount
    room_type = models.CharField(
        max_length=50,
        choices=[
            ("quint", "Quint"),
            ("quad", "Quad"),
            ("triple", "Triple"),
            ("double", "Double"),
            ("sharing", "Sharing"),
            ("all", "All Types"),
        ],
        null=True, blank=True
    )
    per_night_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # store discounted hotels as a proper ManyToMany relation to tickets.Hotels
    discounted_hotels = models.ManyToManyField(
        'tickets.Hotels', related_name='discounts', blank=True
    )

    def __str__(self):
        return f"{self.discount_group.name} - {self.things}"
class Markup(models.Model):
    APPLIES_CHOICES = [
        ("group_ticket", "Group Ticket"),
        ("hotel", "Hotel"),
        ("umrah_package", "Umrah Package"),
    ]

    name = models.CharField(max_length=100)
    applies_to = models.CharField(max_length=20, choices=APPLIES_CHOICES)
    ticket_markup = models.FloatField(default=0, blank=True, null=True)
    hotel_per_night_markup = models.FloatField(default=0, blank=True, null=True)
    umrah_package_markup = models.FloatField(default=0, blank=True, null=True)

    # ab ye sirf organization ki ID store karega, koi relation nahi banega
    organization_id = models.IntegerField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.applies_to})"

from django.db import models
from django.contrib.auth.models import User
from organization.models import Organization, Branch, Agency
from packages.models import TransportSectorPrice, City, Shirka

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

    reseller_commission = models.FloatField(default=0, blank=True, null=True)
    markup_by_reseller = models.FloatField(default=0, blank=True, null=True)

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
    def __str__(self):
        return f"{self.booking} - {self.hotel}"


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
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=50, blank=True, null=True,choices=STATUS_CHOICES)
    # is_price_pkr= models.BooleanField(default=True)
    # riyal_rate = models.FloatField(default=0)


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
    amount = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, default="Pending"
    )  # e.g., Pending, Completed, Failed
    image = models.ImageField(upload_to="media/payment_receipts", blank=True, null=True)
    transaction_number = models.CharField(max_length=100, blank=True, null=True)
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

    main_organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="main_link",null=True,blank=True)
    link_organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="linked_link",null=True,blank=True)
    this_organization_request = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    main_organization_request = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    request_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Main:{self.main_organization.name} Linked:{self.link_organization.name}({self.main_organization_request}/{self.this_organization_request})"
class AllowedReseller(models.Model):
    inventory_owner_company = models.ForeignKey(
        OrganizationLink, on_delete=models.CASCADE, related_name="allowed_resellers"
    )

    reseller_companies = models.ManyToManyField(
        Organization, related_name="reseller_links"
    )

    ALLOWED_CHOICES = [
        ("UMRAH_PACKAGES", "Umrah Packages"),
        ("GROUP_TICKETS", "Group Tickets"),
        ("HOTELS", "Hotels"),
    ]
    allowed =models.CharField(choices=ALLOWED_CHOICES,null=True,blank=True)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]
    requested_status_by_reseller = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )

    discount_group_id=models.IntegerField(blank=True,null=True)
    markup_group_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.inventory_owner_company} → Resellers"
class DiscountGroup(models.Model):
    name = models.CharField(max_length=255)
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

    discounted_hotels = models.IntegerField(blank=True, null=True)

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

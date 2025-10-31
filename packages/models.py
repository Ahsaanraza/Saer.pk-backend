from django.db import models
from organization.models import Organization,Agency
from django.contrib.auth.models import User

# Create your models here.


class RiyalRate(models.Model):
    """
    Model to store the exchange rate of Riyal.
    """

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    rate = models.FloatField(default=0)
    is_visa_pkr = models.BooleanField(default=False)
    is_hotel_pkr = models.BooleanField(default=False)
    is_transport_pkr = models.BooleanField(default=False)
    is_ziarat_pkr = models.BooleanField(default=False)
    is_food_pkr = models.BooleanField(default=False)


class Shirka(models.Model):
    """
    Model to store the details of
    a Shirka.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="shirkas"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SetVisaType(models.Model):
    """
    Model to store the type of visa.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="visa_types"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UmrahVisaPrice(models.Model):
    """
    Model to store the price of Umrah visa.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="umrah_visa_prices"
    )
    visa_type = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    adault_price = models.FloatField(default=0)
    child_price = models.FloatField(default=0)
    infant_price = models.FloatField(default=0)
    maximum_nights = models.IntegerField(default=0)


class UmrahVisaPriceTwo(models.Model):
    """
    Model to store the price of Umrah visa for two categories.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="umrah_visa_prices_two"
    )
    title = models.CharField(max_length=100)
    person_from = models.IntegerField(default=0)  # in months
    person_to = models.IntegerField(default=0)  # in months
    adault_price = models.FloatField(default=0)
    child_price = models.FloatField(default=0)
    infant_price = models.FloatField(default=0)
    is_transport = models.BooleanField(default=False)
    
    vehicle_types = models.ManyToManyField(
        "booking.VehicleType",
        related_name="umrah_visa_prices_two",
        blank=True
    )
    def __str__(self):
        return f"{self.title} ({self.organization.name})"

class UmrahVisaPriceTwoHotel(models.Model):
    """
    Model to store the hotel details for Umrah visa price for two categories.
    """

    umrah_visa_price = models.ForeignKey(
        UmrahVisaPriceTwo, on_delete=models.CASCADE, related_name="hotel_details")
    hotel = models.ForeignKey("tickets.Hotels", on_delete=models.PROTECT)

class OnlyVisaPrice(models.Model):
    """
    Model to store the price of only visa.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="only_visa_prices"
    )
    adault_price = models.FloatField(default=0)
    child_price = models.FloatField(default=0)
    infant_price = models.FloatField(default=0)
    type= models.CharField(max_length=50)
    min_days=models.CharField(max_length=50)
    max_days=models.CharField(max_length=50)
    airpot_name=models.CharField(max_length=100,blank=True, null=True)
    city = models.ForeignKey(
        "City", on_delete=models.CASCADE, related_name="only_visa_prices",blank=True, null=True
    )
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active", blank=True, null=True)

    def __str__(self):
        return f"{self.organization} - {self.city} ({self.type})"



class TransportSectorPrice(models.Model):
    """
    Model to store the details of a Transport Sector.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="transport_sectors"
    )
    reference= models.CharField(max_length=100,default="type1")
    name = models.CharField(max_length=100)
    vehicle_type = models.IntegerField(blank=True, null=True)
    adault_price = models.FloatField(default=0)
    child_price = models.FloatField(default=0)
    infant_price = models.FloatField(default=0)
    is_visa = models.BooleanField(default=False)
    only_transport_charge = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Airlines(models.Model):
    """
    Model to store the details of an Airline.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="airlines"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    logo = models.ImageField(upload_to="media/airlines_logos/", blank=True, null=True)
    is_umrah_seat = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Model to store the details of a City.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="cities"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class FoodPrice(models.Model):
    """
    Model to store the food prices.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="food_prices"
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="food_prices", null=True,blank=True
    )
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100)
    min_pex=models.IntegerField(default=0)  
    per_pex= models.IntegerField(default=0) 
    active = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    def __str__(self):
        return f"({self.city.name})"

class ZiaratPrice(models.Model):
    """
    Model to store the Ziarat prices.
    """
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="ziarat_prices"
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="ziarat_prices", null=True,blank=True
    )
    ziarat_title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    price = models.FloatField(default=0)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active"
    )
    min_pex = models.FloatField(default=0) 
    max_pex = models.FloatField(default=0)
    def __str__(self):
        return f"{self.ziarat_title} ({self.city.name})"

class BookingExpiry(models.Model):
    """
    Model to store the booking expiry time.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="booking_expiries"
    )
    umrah_expiry_time = models.IntegerField(default=0)  # Time in minutes
    ticket_expiry_time = models.IntegerField(default=0)  # Time in minutes


class UmrahPackage(models.Model):
    """
    Model to store the details of an Umrah Package.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="umrah_packages"
    )
    title = models.CharField(max_length=100)
    rules = models.TextField(blank=True, null=True)
    total_seats = models.IntegerField(default=0)
    child_visa_price = models.FloatField(default=0)
    infant_visa_price = models.FloatField(default=0)
    adault_visa_price = models.FloatField(default=0)
    food_price = models.FloatField(default=0)
    makkah_ziyarat_price = models.FloatField(default=0)
    madinah_ziyarat_price = models.FloatField(default=0)
    transport_price = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_quaint_active = models.BooleanField(default=True)
    is_sharing_active = models.BooleanField(default=True)
    is_quad_active = models.BooleanField(default=True)
    is_triple_active = models.BooleanField(default=True)
    is_double_active = models.BooleanField(default=True)
    adault_service_charge = models.FloatField(default=0)
    child_service_charge = models.FloatField(default=0)
    infant_service_charge = models.FloatField(default=0)
    is_service_charge_active = models.BooleanField(default=False)
    adault_partial_payment = models.FloatField(default=0)
    child_partial_payment = models.FloatField(default=0)
    infant_partial_payment = models.FloatField(default=0)
    is_partial_payment_active = models.BooleanField(default=False)
    filght_min_adault_age = models.IntegerField(default=0) 
    filght_max_adault_age = models.IntegerField(default=0) 
    max_chilld_allowed = models.IntegerField(default=0) 
    max_infant_allowed = models.IntegerField(default=0) 
    total_seats = models.BigIntegerField(default=0, blank=True, null=True)
    left_seats = models.BigIntegerField(default=0, blank=True, null=True)
    booked_seats = models.BigIntegerField(default=0, blank=True, null=True)
    confirmed_seats = models.BigIntegerField(default=0, blank=True, null=True)
    inventory_owner_organization_id = models.IntegerField(blank=True, null=True)
    # Whether this package may be resold by allowed resellers
    reselling_allowed = models.BooleanField(default=False)
    # Public visibility and availability window for public bookings
    is_public = models.BooleanField(default=False)
    available_start_date = models.DateField(blank=True, null=True)
    available_end_date = models.DateField(blank=True, null=True)
    # canonical per-person price used for public bookings
    price_per_person = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    # Minimum partial payment rules (can be organization-specific too)
    min_partial_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    min_partial_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Commission configuration
    # Area Agent Commission per pax type
    area_agent_commission_adult = models.FloatField(default=0, blank=True, null=True)
    area_agent_commission_child = models.FloatField(default=0, blank=True, null=True)
    area_agent_commission_infant = models.FloatField(default=0, blank=True, null=True)

    # Branch Commission per pax type
    branch_commission_adult = models.FloatField(default=0, blank=True, null=True)
    branch_commission_child = models.FloatField(default=0, blank=True, null=True)
    branch_commission_infant = models.FloatField(default=0, blank=True, null=True)



class UmrahPackageHotelDetails(models.Model):
    package = models.ForeignKey(
        UmrahPackage, on_delete=models.CASCADE, related_name="hotel_details"
    )
    hotel = models.ForeignKey("tickets.Hotels", on_delete=models.PROTECT)
    check_in_date=models.DateField(blank=True, null=True)
    check_out_date=models.DateField(blank=True, null=True)
    number_of_nights = models.IntegerField(default=0)
    quaint_bed_price = models.FloatField(default=0)
    sharing_bed_price = models.FloatField(default=0)
    quad_bed_price = models.FloatField(default=0)
    triple_bed_price = models.FloatField(default=0)
    double_bed_price = models.FloatField(default=0)

class UmrahPackageTransportDetails(models.Model):
    package = models.ForeignKey(
        UmrahPackage, on_delete=models.CASCADE, related_name="transport_details"
    )
    transport_sector = models.ForeignKey(
        TransportSectorPrice, on_delete=models.PROTECT, blank=True, null=True
    )   
    vehicle_type = models.IntegerField(blank=True, null=True)
    transport_type = models.CharField(max_length=255, blank=True, null=True)

class UmrahPackageTicketDetails(models.Model):
    package= models.ForeignKey(
        UmrahPackage, on_delete=models.CASCADE, related_name="ticket_details")
    ticket= models.ForeignKey("tickets.Ticket", on_delete=models.PROTECT)

class UmrahPackageDiscountDetails(models.Model):
    package= models.ForeignKey(
        UmrahPackage, on_delete=models.CASCADE, related_name="discount_details")
    adault_from= models.IntegerField(default=0) 
    adault_to= models.IntegerField(default=0)  
    max_discount= models.FloatField(default=0)  

class  CustomUmrahPackage(models.Model):
    """
    Model to store the details of a Custom Umrah Package.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="custom_umrah_packages"
    )
    # agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="custom_umrah_packages")
    agency= models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="custom_umrah_packages")
    user = models.ForeignKey(   # 👈 naya field
        User, on_delete=models.CASCADE, related_name="custom_umrah_packages", blank=True, null=True
    )
    total_adaults = models.IntegerField(default=0)
    total_children = models.IntegerField(default=0)
    total_infants = models.IntegerField(default=0)
    child_visa_price = models.FloatField(default=0)
    infant_visa_price = models.FloatField(default=0)
    adault_visa_price = models.FloatField(default=0) 
    long_term_stay = models.BooleanField(default=False)
    is_full_transport = models.BooleanField(default=False)
    is_one_side_transport = models.BooleanField(default=False)
    only_visa = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)



class CustomUmrahPackageHotelDetails(models.Model):
    package = models.ForeignKey(
        CustomUmrahPackage, on_delete=models.CASCADE, related_name="hotel_details"
    )
    hotel = models.ForeignKey("tickets.Hotels", on_delete=models.PROTECT)
    room_type = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.FloatField(default=0)
    sharing_type = models.CharField(max_length=20, blank=True, null=True)
    check_in_date=models.DateField(blank=True, null=True)
    check_out_date=models.DateField(blank=True, null=True)
    number_of_nights = models.IntegerField(default=0)
    special_request = models.TextField(blank=True, null=True)
    price= models.FloatField(default=0)

class CustomUmrahPackageTransportDetails(models.Model):
    package = models.ForeignKey(
        CustomUmrahPackage, on_delete=models.CASCADE, related_name="transport_details"
    )
    # transport_sector = models.ForeignKey(
    #     TransportSectorPrice, on_delete=models.PROTECT
    # )   
    vehicle_type = models.IntegerField(blank=True, null=True)


class CustomUmrahPackageTicketDetails(models.Model):
    package= models.ForeignKey(
        CustomUmrahPackage, on_delete=models.CASCADE, related_name="ticket_details")
    ticket= models.ForeignKey("tickets.Ticket", on_delete=models.PROTECT)


class CustomUmrahZiaratDetails(models.Model):
    package = models.ForeignKey(
        CustomUmrahPackage, on_delete=models.CASCADE, related_name="ziarat_details"
    )
    ziarat = models.ForeignKey(ZiaratPrice, on_delete=models.PROTECT)

class CustomUmrahFoodDetails(models.Model):
    package = models.ForeignKey(
        CustomUmrahPackage, on_delete=models.CASCADE, related_name="food_details"
    )
    food = models.ForeignKey(FoodPrice, on_delete=models.PROTECT)

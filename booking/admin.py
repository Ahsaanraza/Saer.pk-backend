from django.contrib import admin
from .models import Booking, Discount, DiscountGroup, Markup, BankAccount, AllowedReseller, BookingHotelDetails, BookingPersonDetail, BookingTicketDetails

admin.site.register(Booking)
admin.site.register(Discount)
admin.site.register(DiscountGroup)
admin.site.register(Markup)
admin.site.register(BankAccount)
admin.site.register(AllowedReseller)
admin.site.register(BookingHotelDetails)
admin.site.register(BookingPersonDetail)
admin.site.register(BookingTicketDetails)

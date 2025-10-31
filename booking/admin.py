from django.contrib import admin
from .models import (
	Booking,
	Discount,
	DiscountGroup,
	Markup,
	BankAccount,
	AllowedReseller,
	BookingHotelDetails,
	BookingPersonDetail,
	BookingTicketDetails,
	HotelOutsourcing,
)


class BookingPersonDetailInline(admin.TabularInline):
	model = BookingPersonDetail
	extra = 0
	fields = (
		'first_name', 'last_name', 'person_title', 'age_group', 'contact_number', 'passport_number', 'ticket_price',
	)
	readonly_fields = ('first_name', 'last_name', 'passport_number')


class BookingAdmin(admin.ModelAdmin):
	list_display = (
		'booking_number', 'invoice_no', 'status', 'is_paid', 'total_pax', 'total_amount', 'paid_payment', 'pending_payment', 'created_at', 'is_public_booking'
	)
	search_fields = ('booking_number', 'invoice_no', 'person_details__first_name', 'person_details__passport_number')
	list_filter = ('status', 'is_paid', 'is_public_booking')
	inlines = [BookingPersonDetailInline]
	readonly_fields = ('booking_number', 'invoice_no')


class BookingPersonDetailAdmin(admin.ModelAdmin):
	list_display = ('booking', 'first_name', 'last_name', 'passport_number', 'contact_number', 'age_group', 'ticket_price')
	search_fields = ('first_name', 'last_name', 'passport_number', 'contact_number')
	list_filter = ('age_group',)


class HotelOutsourcingAdmin(admin.ModelAdmin):
	list_display = ("booking", "hotel_name", "is_paid", "agent_notified", "created_at")
	search_fields = ("booking__booking_number", "hotel_name")
	list_filter = ("is_paid", "agent_notified")


admin.site.register(Booking, BookingAdmin)
admin.site.register(Discount)
admin.site.register(DiscountGroup)
admin.site.register(Markup)
admin.site.register(BankAccount)
admin.site.register(AllowedReseller)
admin.site.register(BookingHotelDetails)
admin.site.register(BookingPersonDetail, BookingPersonDetailAdmin)
admin.site.register(BookingTicketDetails)
admin.site.register(HotelOutsourcing, HotelOutsourcingAdmin)

from django.contrib import admin
from .models import (
	Ticket,
	TicketTripDetails,
	TickerStopoverDetails,
	Hotels,
	HotelPrices,
	HotelContactDetails,
	HotelRooms,
	RoomDetails,
	HotelPhoto,
)


admin.site.register(Ticket)
admin.site.register(TicketTripDetails)
admin.site.register(TickerStopoverDetails)
admin.site.register(Hotels)
admin.site.register(HotelPrices)
admin.site.register(HotelContactDetails)
admin.site.register(HotelRooms)
admin.site.register(RoomDetails)
admin.site.register(HotelPhoto)

from django.contrib import admin
from .models import (
	UmrahPackage,
	UmrahPackageHotelDetails,
	UmrahPackageTicketDetails,
	UmrahPackageTransportDetails,
	UmrahPackageDiscountDetails,
	CustomUmrahPackage,
	CustomUmrahPackageHotelDetails,
	CustomUmrahPackageTicketDetails,
	CustomUmrahPackageTransportDetails,
)


admin.site.register(UmrahPackage)
admin.site.register(UmrahPackageHotelDetails)
admin.site.register(UmrahPackageTicketDetails)
admin.site.register(UmrahPackageTransportDetails)
admin.site.register(UmrahPackageDiscountDetails)
# Optional: register custom package models
admin.site.register(CustomUmrahPackage)
admin.site.register(CustomUmrahPackageHotelDetails)
admin.site.register(CustomUmrahPackageTicketDetails)
admin.site.register(CustomUmrahPackageTransportDetails)

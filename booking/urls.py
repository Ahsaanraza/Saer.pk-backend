from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookingViewSet,PaymentViewSet, SectorViewSet,BigSectorViewSet, VehicleTypeViewSet, InternalNoteViewSet, BankAccountViewSet, OrganizationLinkViewSet, AllowedResellerViewSet, DiscountGroupViewSet, MarkupViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'big-sectors', BigSectorViewSet, basename='big-sector')
router.register(r'vehicle-types', VehicleTypeViewSet, basename='vehicle-types')
router.register(r'internal-notes', InternalNoteViewSet, basename="internal-notes")
router.register(r'organization-links', OrganizationLinkViewSet, basename='organization-link')
router.register(r'allowed-resellers', AllowedResellerViewSet, basename='allowed-resellers')
router.register(r'discount-groups', DiscountGroupViewSet, basename="discount-groups")
router.register(r'bank-accounts', BankAccountViewSet, basename='bank-accounts')
router.register(r"markups", MarkupViewSet, basename="markup")
urlpatterns = [
    path('api/', include(router.urls)),
]

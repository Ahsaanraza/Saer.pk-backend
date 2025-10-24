from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, HotelsViewSet, HotelRoomsViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='tickets')
router.register(r'hotels', HotelsViewSet, basename='hotels')
router.register(r'hotel-rooms', HotelRoomsViewSet, basename='hotelrooms')

urlpatterns = [
    path('api/', include(router.urls)),  # ✅ your app’s API is now under /api/
]

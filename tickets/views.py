from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from .models import Ticket, Hotels,HotelRooms
from .serializers import TicketSerializer, HotelsSerializer, HotelRoomsSerializer


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")

        query_filter = Q()
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        else:
            query_filter = Q(organization_id=organization_id)

        queryset = Ticket.objects.filter(query_filter)

        return queryset


class HotelsViewSet(ModelViewSet):
    serializer_class = HotelsSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")

        query_filter = Q()
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        else:
            query_filter = Q(organization_id=organization_id)

        queryset = Hotels.objects.filter(query_filter).prefetch_related('prices', 'contact_details')

        return queryset


class HotelRoomsViewSet(ModelViewSet):
    serializer_class = HotelRoomsSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        hotel_id = self.request.query_params.get("hotel_id")

        query_filter = Q()
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        else:
            query_filter = Q(hotel__organization_id=organization_id)

        if hotel_id:
            query_filter &= Q(hotel_id=hotel_id)
            
        queryset = HotelRooms.objects.filter(query_filter).select_related('hotel')

        return queryset
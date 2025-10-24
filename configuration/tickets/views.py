from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone

from .models import Ticket, Hotels,HotelRooms
from .serializers import TicketSerializer, HotelsSerializer, HotelRoomsSerializer
from booking.models import AllowedReseller


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")

        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        
        today=timezone.now().date()
        allowed_inventory_orgs=(AllowedReseller.objects.filter(
            reseller_companies__id=organization_id,
            requested_status_by_reseller="ACCEPTED"
        ).values_list('inventory_owner_company__id',flat=True))
        allowed_orgs=list(allowed_inventory_orgs)+[int(organization_id)]

        query_filter = Q(organization_id__in=allowed_orgs) &  Q(
            is_active=True,
            available_seats__gt=0,
            reselling_allowed=True,
            end_date__gte=today
        )

        queryset = Ticket.objects.filter(query_filter)

        return queryset
    
    def perform_create(self, serializer):
        """Automatically set owner and organization from query param."""
        organization_id = self.request.query_params.get("organization")

        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")

        from organization.models import Organization
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            raise PermissionDenied("Invalid organization ID.")

        serializer.save(
            owner_organization=organization,
            organization=organization
        )


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
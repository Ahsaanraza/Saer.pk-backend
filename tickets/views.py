from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from .models import Ticket, Hotels,HotelRooms
from booking.models import AllowedReseller
from .serializers import TicketSerializer, HotelsSerializer, HotelRoomsSerializer
from django.utils import timezone


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")

        query_filter = Q()
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        else:
            # start with tickets published by the caller org
            query_filter = Q(organization_id=organization_id)

        # Build allowed owner organization ids based on AllowedReseller entries
        allowed_owner_org_ids = []
        try:
            allowed_qs = AllowedReseller.objects.filter(
                reseller_company_id=organization_id,
                requested_status_by_reseller="ACCEPTED",
            )
            # filter by allowed_types containing GROUP_TICKETS
            for ar in allowed_qs:
                inv = getattr(ar, "inventory_owner_company", None)
                if inv is None:
                    continue
                org_id = getattr(inv, "organization_id", None) or getattr(inv, "main_organization_id", None) or None
                if org_id:
                    types = ar.allowed_types or []
                    if "GROUP_TICKETS" in types:
                        allowed_owner_org_ids.append(org_id)

        except Exception:
            allowed_owner_org_ids = []

        # Include own organization as owner as well
        own_org_id = int(organization_id)
        owner_ids = set(allowed_owner_org_ids + [own_org_id])

        # Base queryset: tickets that belong to owner ids (either owned or published by allowed owners)
        queryset = Ticket.objects.filter(
            Q(organization_id__in=owner_ids) | Q(owner_organization_id__in=owner_ids)
        )

        # Exclude inactive tickets (status == 'inactive')
        queryset = queryset.exclude(status="inactive")

        # Exclude tickets with no available seats
        queryset = queryset.filter(left_seats__gt=0)

        # Exclude tickets with passed departure dates (use trip_details)
        now = timezone.now()
        queryset = queryset.filter(trip_details__departure_date_time__gte=now)

        # For reseller callers (non-owner), ensure reselling_allowed=True
        queryset = queryset.filter(
            Q(organization_id=own_org_id) |
            (Q(reselling_allowed=True))
        ).distinct()

        return queryset


class HotelsViewSet(ModelViewSet):
    serializer_class = HotelsSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")

        query_filter = Q()
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        else:
            # Build allowed owner organization ids based on AllowedReseller entries
            allowed_owner_org_ids = []
            try:
                allowed_qs = AllowedReseller.objects.filter(
                    reseller_company_id=organization_id,
                    requested_status_by_reseller="ACCEPTED",
                )
                # filter by allowed_types containing HOTELS
                for ar in allowed_qs:
                    # depending on legacy structure, inventory_owner_company may be an OrganizationLink
                    inv = getattr(ar, "inventory_owner_company", None)
                    if inv is None:
                        continue
                    # try to get organization id from possible fields
                    org_id = getattr(inv, "organization_id", None) or getattr(inv, "main_organization_id", None) or getattr(inv, "main_organization_id", None)
                    if org_id:
                        # only include if allowed_types mention HOTELS
                        types = ar.allowed_types or []
                        if "HOTELS" in types:
                            allowed_owner_org_ids.append(org_id)

            except Exception:
                allowed_owner_org_ids = []

            # include own organization
            own_org_id = int(organization_id)
            owner_ids = set(allowed_owner_org_ids + [own_org_id])

            # Only active hotels
            queryset = Hotels.objects.filter(is_active=True)

            # Only hotels belonging to owner_ids
            queryset = queryset.filter(organization_id__in=owner_ids)

            # For reseller (non-own), exclude hotels that are not resellable or that have no shareable prices
            # If requested organization is not the owner, ensure reselling_allowed=True and at least one price with is_sharing_allowed=True
            queryset = queryset.prefetch_related('prices', 'contact_details')
            # If caller is reseller (not owner), apply extra filters
            # Note: filter keeps hotels owned by own_org_id even if not resellable
            queryset = queryset.filter(
                Q(organization_id=own_org_id) |
                (Q(reselling_allowed=True) & Q(prices__is_sharing_allowed=True))
            ).distinct()

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
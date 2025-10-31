from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import (
    RiyalRate,
    Shirka,
    UmrahVisaPrice,
    UmrahVisaPriceTwo,
    TransportSectorPrice,
    Airlines,
    City,
    BookingExpiry,
    UmrahPackage,
    CustomUmrahPackage,
    OnlyVisaPrice,
    SetVisaType,
    FoodPrice,
    ZiaratPrice,
)
from .serializers import (
    RiyalRateSerializer,
    ShirkaSerializer,
    UmrahVisaPriceSerializer,
    UmrahVisaPriceTwoSerializer,
    TransportSectorPriceSerializer,
    AirlinesSerializer,
    CitySerializer,
    BookingExpirySerializer,
    UmrahPackageSerializer,
    CustomUmrahPackageSerializer,
    OnlyVisaPriceSerializer,
    SetVisaTypeSerializer,
    FoodPriceSerializer,
    ZiaratPriceSerializer,
)
from tickets.models import Ticket, Hotels
from tickets.serializers import TicketSerializer, HotelsSerializer
from django.db.models import Q
from booking.models import AllowedReseller
from django.utils import timezone
from rest_framework import generics
from .serializers import PublicUmrahPackageListSerializer, PublicUmrahPackageDetailSerializer
from django.utils.text import slugify


class RiyalRateViewSet(ModelViewSet):
    serializer_class = RiyalRateSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return RiyalRate.objects.filter(organization_id=organization_id)


class ShirkaViewSet(ModelViewSet):
    serializer_class = ShirkaSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return Shirka.objects.filter(organization_id=organization_id)


class UmrahVisaPriceViewSet(ModelViewSet):
    serializer_class = UmrahVisaPriceSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return UmrahVisaPrice.objects.filter(organization_id=organization_id)


class UmrahVisaPriceTwoViewSet(ModelViewSet):
    serializer_class = UmrahVisaPriceTwoSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return UmrahVisaPriceTwo.objects.filter(organization_id=organization_id)


class OnlyVisaPriceViewSet(ModelViewSet):
    serializer_class = OnlyVisaPriceSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return OnlyVisaPrice.objects.filter(organization_id=organization_id)

class TransportSectorPriceViewSet(ModelViewSet):
    serializer_class = TransportSectorPriceSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return TransportSectorPrice.objects.filter(organization_id=organization_id)


class AirlinesViewSet(ModelViewSet):
    serializer_class = AirlinesSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return Airlines.objects.filter(organization_id=organization_id)


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return City.objects.filter(organization_id=organization_id)

class FoodPriceViewSet(ModelViewSet):
    serializer_class = FoodPriceSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return FoodPrice.objects.filter(organization_id=organization_id)
class ZiaratPriceViewSet(ModelViewSet):
    serializer_class = ZiaratPriceSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return ZiaratPrice.objects.filter(organization_id=organization_id)

class BookingExpiryViewSet(ModelViewSet):
    serializer_class = BookingExpirySerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return BookingExpiry.objects.filter(organization_id=organization_id)


class UmrahPackageViewSet(ModelViewSet):
    serializer_class = UmrahPackageSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        is_active = self.request.query_params.get("is_active")

        # Build allowed owner organization ids based on AllowedReseller entries
        allowed_owner_org_ids = []
        try:
            allowed_qs = AllowedReseller.objects.filter(
                reseller_company_id=organization_id,
                requested_status_by_reseller="ACCEPTED",
            )
            for ar in allowed_qs:
                inv = getattr(ar, "inventory_owner_company", None)
                if inv is None:
                    continue
                org_id = getattr(inv, "organization_id", None) or getattr(inv, "main_organization_id", None) or None
                if org_id:
                    types = ar.allowed_types or []
                    if "UMRAH_PACKAGES" in types:
                        allowed_owner_org_ids.append(org_id)
        except Exception:
            allowed_owner_org_ids = []

        own_org_id = int(organization_id)
        owner_ids = set(allowed_owner_org_ids + [own_org_id])

        query_filter = Q()
        # include packages published by owner_ids or whose inventory_owner_organization_id is in owner_ids
        query_filter &= (Q(organization_id__in=owner_ids) | Q(inventory_owner_organization_id__in=owner_ids))
        if is_active is not None:
            # accept 'true'/'false' strings
            if isinstance(is_active, str):
                is_active_val = is_active.lower() in ("1", "true", "yes")
            else:
                is_active_val = bool(is_active)
            query_filter &= Q(is_active=is_active_val)

        queryset = UmrahPackage.objects.filter(query_filter).prefetch_related(
            "hotel_details__hotel",
            "transport_details__transport_sector",
            "ticket_details__ticket",
            "discount_details",
        )

        # Exclude packages whose ticket departures have already passed.
        # If a package has no tickets, the passed-date rule should NOT apply (keep such packages).
        now = timezone.now()
        # exclude packages where any ticket's trip details show a departure < now
        queryset = queryset.exclude(ticket_details__ticket__trip_details__departure_date_time__lt=now)

        # For reseller callers (non-owner), ensure reselling_allowed=True OR package belongs to own_org
        queryset = queryset.filter(
            Q(organization_id=own_org_id) | Q(reselling_allowed=True)
        ).distinct()
        return queryset
    @action(detail=False, methods=["get"])
    def get_by_id(self, request):
        package_id = request.query_params.get("id")
        if not package_id:
            return Response(
                {"error": "Missing 'id' query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            package = UmrahPackage.objects.prefetch_related(
                "hotel_details__hotel",
                "transport_details__transport_sector",
                "ticket_details__ticket",
                "discount_details",
            ).get(id=package_id)
        except UmrahPackage.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(package)
        return Response(serializer.data)


class CustomUmrahPackageViewSet(ModelViewSet):
    serializer_class = CustomUmrahPackageSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        
        query_filter = Q()
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        
        queryset = CustomUmrahPackage.objects.filter(query_filter).select_related("agency").prefetch_related(
            "hotel_details__hotel",
            "transport_details__transport_sector",
            "ticket_details__ticket",
        )
        return queryset

class SetVisaTypeViewSet(ModelViewSet):
    serializer_class = SetVisaTypeSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization")
        if not organization_id:
            raise PermissionDenied("Missing 'organization' query parameter.")
        return SetVisaType.objects.filter(organization_id=organization_id)



class AllPricesAPIView(APIView):
    def get(self, request):
        organization_id = request.query_params.get("organization_id")
        if not organization_id:
            return Response({"error": "organization_id is required"}, status=400)

        # apply filter on all models
        data = {
            "riyal_rates": RiyalRate.objects.filter(organization_id=organization_id).values(),
            "shirkas": Shirka.objects.filter(organization_id=organization_id).values(),
            "umrah_visa_prices": UmrahVisaPrice.objects.filter(organization_id=organization_id).values(),
            "umrah_visa_type_two": UmrahVisaPriceTwo.objects.filter(organization_id=organization_id).values(),
            "only_visa_prices": OnlyVisaPrice.objects.filter(organization_id=organization_id).values(),
            # "transport_sector_prices": TransportSectorPrice.objects.filter(organization_id=organization_id).values(),
            "airlines": Airlines.objects.filter(organization_id=organization_id).values(),
            "cities": City.objects.filter(organization_id=organization_id).values(),
            "set_visa_type": SetVisaType.objects.filter(organization_id=organization_id).values(),
            "food_prices": FoodPrice.objects.filter(organization_id=organization_id, active=True).values(),
            "ziarat_prices": ZiaratPrice.objects.filter(organization_id=organization_id).values(),
            "tickets": TicketSerializer(
                Ticket.objects.filter(organization_id=organization_id), many=True
            ).data,
            "hotels": HotelsSerializer(
                Hotels.objects.filter(organization_id=organization_id), many=True
            ).data,
        }

        return Response(data)


class PublicUmrahPackageListAPIView(generics.ListAPIView):
    """Public list of Umrah packages (read-only)."""
    serializer_class = PublicUmrahPackageListSerializer

    def get_queryset(self):
        today = timezone.now().date()
        qs = UmrahPackage.objects.filter(
            is_active=True, is_public=True
        )
        # apply date window if fields present
        qs = qs.filter(
            Q(available_start_date__isnull=True) | Q(available_start_date__lte=today),
            Q(available_end_date__isnull=True) | Q(available_end_date__gte=today),
        )

        # filters
        city = self.request.query_params.get("city")
        if city:
            qs = qs.filter(hotel_details__hotel__city_id=city)

        duration = self.request.query_params.get("duration")
        if duration:
            try:
                dur = int(duration)
                qs = qs.filter(hotel_details__number_of_nights=dur)
            except Exception:
                pass

        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")
        if price_min:
            try:
                qs = qs.filter(Q(price_per_person__gte=price_min) | Q(adault_visa_price__gte=price_min))
            except Exception:
                pass
        if price_max:
            try:
                qs = qs.filter(Q(price_per_person__lte=price_max) | Q(adault_visa_price__lte=price_max))
            except Exception:
                pass

        hotel_star = self.request.query_params.get("hotel_star")
        if hotel_star:
            qs = qs.filter(hotel_details__hotel__star_rating=hotel_star)

        availability = self.request.query_params.get("availability")
        if availability and availability.lower() in ("1", "true", "yes"):
            qs = qs.filter(left_seats__gt=0)

        return qs.distinct()


class PublicUmrahPackageDetailAPIView(APIView):
    """Public package detail view. Lookup by id or slug (slugified title)."""

    def get(self, request, identifier):
        # try id
        pkg = None
        try:
            if identifier.isdigit():
                pkg = UmrahPackage.objects.get(id=int(identifier), is_active=True, is_public=True)
        except UmrahPackage.DoesNotExist:
            pkg = None

        if pkg is None:
            # try slug match on title
            sl = identifier
            qs = UmrahPackage.objects.filter(is_active=True, is_public=True)
            for p in qs:
                if slugify(p.title) == sl:
                    pkg = p
                    break

        if not pkg:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PublicUmrahPackageDetailSerializer(pkg)
        return Response(serializer.data)

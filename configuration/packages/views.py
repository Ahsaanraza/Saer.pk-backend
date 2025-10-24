from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
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

        query_filter = Q()

        if organization_id:
            query_filter &= Q(organization_id=organization_id)
        if is_active is not None:
            query_filter &= Q(is_active=is_active)

        queryset = UmrahPackage.objects.filter(query_filter).prefetch_related(
            "hotel_details__hotel",
            "transport_details__transport_sector",
            "ticket_details__ticket",
            "discount_details",
        )
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

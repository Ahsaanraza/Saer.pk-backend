# PaxMovement API endpoints
from .models import PaxMovement
from .serializers import PaxMovementSerializer
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

class PaxMovementViewSet(viewsets.ModelViewSet):
    queryset = PaxMovement.objects.all().order_by('-created_at')
    serializer_class = PaxMovementSerializer

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        obj = self.get_object()
        return Response({"status": obj.status, "verified_exit": obj.verified_exit})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        qs = PaxMovement.objects.all()
        summary = {
            "in_pakistan": qs.filter(status="in_pakistan").count(),
            "entered_ksa": qs.filter(status="entered_ksa").count(),
            "in_ksa": qs.filter(status="in_ksa").count(),
            "exited_ksa": qs.filter(status="exited_ksa").count(),
            "exit_pending": qs.filter(status="exit_pending").count(),
        }
        # City breakdown if available
        city_counts = list(qs.values('arrival_airport').annotate(count=Count('id')).order_by('-count'))
        summary["by_city"] = city_counts
        return Response(summary)

    @action(detail=True, methods=['post'])
    def verify_exit(self, request, pk=None):
        obj = self.get_object()
        obj.status = "exited_ksa"
        obj.verified_exit = True
        obj.save()
        return Response({"message": "Exit verified", "status": obj.status, "verified_exit": obj.verified_exit})

    @action(detail=True, methods=['post'])
    def notify_agent(self, request, pk=None):
        obj = self.get_object()
        # Placeholder: In production, send notification to agent
        # e.g., send_mail(subject, message, ...)
        return Response({"message": f"Agent {obj.agent_id} notified to update flight info for pax {obj.pax_id}"})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import UniversalRegistration, RegistrationRule
from .serializers import UniversalRegistrationSerializer, RegistrationRuleSerializer
from .utils import generate_prefixed_id
from .permissions import UniversalPermission
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q


class UniversalRegisterView(generics.CreateAPIView):
    serializer_class = UniversalRegistrationSerializer
    queryset = UniversalRegistration.objects.all()
    permission_classes = (IsAuthenticated, UniversalPermission)

    def perform_create(self, serializer):
        # Generate atomic prefixed ID using utils
        t = serializer.validated_data.get("type")
        if not t:
            generated_id = generate_prefixed_id("generic")
        else:
            generated_id = generate_prefixed_id(t)

        serializer.save(id=generated_id)

    def create(self, request, *args, **kwargs):
        # Override to match the response contract: message + data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": f"{serializer.validated_data.get('type', 'Entity').capitalize()} registered successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UniversalListView(generics.ListAPIView):
    serializer_class = UniversalRegistrationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = UniversalRegistration.objects.filter(is_active=True)
        t = self.request.query_params.get("type")
        parent_id = self.request.query_params.get("parent_id")
        status = self.request.query_params.get("status")
        search = self.request.query_params.get("search")

        if t:
            qs = qs.filter(type=t)
        if parent_id:
            qs = qs.filter(parent__id=parent_id)
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(contact_no__icontains=search)
                | Q(email__icontains=search)
                | Q(id__icontains=search)
            )

        # pagination handled by DRF settings if configured
        return qs


class UniversalDetailView(generics.RetrieveAPIView):
    serializer_class = UniversalRegistrationSerializer
    lookup_field = "id"
    queryset = UniversalRegistration.objects.all()
    permission_classes = (IsAuthenticated,)


class UniversalUpdateView(generics.UpdateAPIView):
    serializer_class = UniversalRegistrationSerializer
    lookup_field = "id"
    queryset = UniversalRegistration.objects.all()
    permission_classes = (IsAuthenticated, UniversalPermission)


class UniversalDeleteView(APIView):
    def delete(self, request, id):
        obj = get_object_or_404(UniversalRegistration, id=id)
        # Use model cascade deactivation which saves objects (signals will log)
        performed_by = None
        if request.user and request.user.is_authenticated:
            performed_by = getattr(request.user, "username", str(request.user))
        obj.deactivate_with_cascade(performed_by=performed_by)
        return Response({"message": "Deleted (soft, cascaded)"}, status=status.HTTP_200_OK)



# RegistrationRule CRUD API
from rest_framework import viewsets
from .models import RegistrationRule
from .serializers import RegistrationRuleSerializer

class RegistrationRuleViewSet(viewsets.ModelViewSet):
    queryset = RegistrationRule.objects.all().order_by('-created_at')
    serializer_class = RegistrationRuleSerializer

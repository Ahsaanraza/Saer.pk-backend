from rest_framework import viewsets
from .serializers import OrganizationSerializer, BranchSerializer, AgencySerializer
from .models import Organization, Branch, Agency
from django.db.models import Q


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if user_id:
            query_filters &= Q(user=user_id)
        queryset = Organization.objects.filter(query_filters)
        return queryset


class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization_id")
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if organization_id:
            query_filters &= Q(organization_id=organization_id)
        if user_id:
            query_filters &= Q(user=user_id)
        queryset = Branch.objects.filter(query_filters).select_related("organization")
        return queryset


class AgencyViewSet(viewsets.ModelViewSet):
    serializer_class = AgencySerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization_id")
        branch_id = self.request.query_params.get("branch_id")
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if organization_id:
            query_filters &= Q(branch__organization_id=organization_id)
        if branch_id:
            query_filters &= Q(branch_id=branch_id)
        if user_id:
            query_filters &= Q(user=user_id)
        queryset = Agency.objects.filter(query_filters).select_related("branch").prefetch_related("files")
        return queryset
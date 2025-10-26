from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Organization, Branch, Agency, OrganizationLink
from .serializers import (
    OrganizationSerializer,
    BranchSerializer,
    AgencySerializer,
    OrganizationLinkSerializer,
)


class OrganizationLinkViewSet(viewsets.ModelViewSet):
    """
    Manage linking between organizations.
    - Only Super Admins can create link requests.
    - Both organizations must accept for request_status to become True.
    - Either side can reject.
    """
    serializer_class = OrganizationLinkSerializer
    queryset = OrganizationLink.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Allow filtering links by organization_id"""
        organization_id = self.request.query_params.get("organization_id")
        queryset = self.queryset
        if organization_id:
            queryset = queryset.filter(
                Q(main_organization_id=organization_id) |
                Q(link_organization_id=organization_id)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        """Only Super Admin can create new organization link"""
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only Super Admins can create organization links."},
                status=status.HTTP_403_FORBIDDEN,
            )

        main_org_id = request.data.get("Main_organization_id")
        link_org_id = request.data.get("Link_organization_id")

        if not (main_org_id and link_org_id):
            return Response(
                {"detail": "Both Main_organization_id and Link_organization_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            main_org = Organization.objects.get(id=main_org_id)
            link_org = Organization.objects.get(id=link_org_id)
        except Organization.DoesNotExist:
            return Response(
                {"detail": "One or both organizations not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        link = OrganizationLink.objects.create(
            main_organization=main_org,
            link_organization=link_org,
            link_organization_request=OrganizationLink.STATUS_PENDING,
            main_organization_request=OrganizationLink.STATUS_PENDING,
            request_status=False,
        )

        serializer = self.get_serializer(link)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        """Accept link request — either main or link organization can do this."""
        link = self.get_object()
        user = request.user
        user_orgs = user.organizations.all()

        if link.main_organization in user_orgs:
            link.main_organization_request = OrganizationLink.STATUS_ACCEPTED
        elif link.link_organization in user_orgs:
            link.link_organization_request = OrganizationLink.STATUS_ACCEPTED
        else:
            return Response(
                {"detail": "You are not a member of either linked organization."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Auto-set request_status = True when both accepted
        if (
            link.main_organization_request == OrganizationLink.STATUS_ACCEPTED
            and link.link_organization_request == OrganizationLink.STATUS_ACCEPTED
        ):
            link.request_status = True
        else:
            link.request_status = False

        link.save()
        return Response(self.get_serializer(link).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Reject link request — any side can reject, making request_status False."""
        link = self.get_object()
        user = request.user
        user_orgs = user.organizations.all()

        if link.main_organization in user_orgs:
            link.main_organization_request = OrganizationLink.STATUS_REJECTED
        elif link.link_organization in user_orgs:
            link.link_organization_request = OrganizationLink.STATUS_REJECTED
        else:
            return Response(
                {"detail": "You are not a member of either linked organization."},
                status=status.HTTP_403_FORBIDDEN,
            )

        link.request_status = False
        link.save()
        return Response(self.get_serializer(link).data, status=status.HTTP_200_OK)


# -------------------------------------------------------------------
# Other APIs (Organization, Branch, Agency)
# -------------------------------------------------------------------

class OrganizationViewSet(viewsets.ModelViewSet):
    """API for managing Organizations"""
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if user_id:
            query_filters &= Q(user=user_id)
        return Organization.objects.filter(query_filters)


class BranchViewSet(viewsets.ModelViewSet):
    """API for managing Branches"""
    serializer_class = BranchSerializer

    def get_queryset(self):
        organization_id = self.request.query_params.get("organization_id")
        user_id = self.request.query_params.get("user_id")
        query_filters = Q()
        if organization_id:
            query_filters &= Q(organization_id=organization_id)
        if user_id:
            query_filters &= Q(user=user_id)
        return Branch.objects.filter(query_filters).select_related("organization")


class AgencyViewSet(viewsets.ModelViewSet):
    """API for managing Agencies"""
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
        return Agency.objects.filter(query_filters).select_related("branch").prefetch_related("files")

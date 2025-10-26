from django.urls import path, include
from .views import OrganizationViewSet, BranchViewSet,AgencyViewSet, OrganizationLinkViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"organizations", OrganizationViewSet, basename="organizations")
router.register(r"branches", BranchViewSet, basename="branches")
router.register(r"agencies", AgencyViewSet, basename="agencies")
router.register(r"organization-links", OrganizationLinkViewSet, basename="organization-links")


urlpatterns = [
    path("api/", include(router.urls)),
]

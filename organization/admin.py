from django.contrib import admin
from .models import OrganizationLink, Branch, Agency, Organization

# Register OrganizationLink
@admin.register(OrganizationLink)
class OrganizationLinkAdmin(admin.ModelAdmin):
	# Use fields that exist on the OrganizationLink model
	list_display = (
		"main_organization",
		"link_organization",
		"link_organization_request",
		"main_organization_request",
		"request_status",
		"created_at",
	)
	list_filter = ("request_status", "link_organization_request", "main_organization_request")
	search_fields = ("main_organization__name", "link_organization__name")


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "organization", "contact_number", "email", "commission_id")
	search_fields = ("name", "organization__name", "commission_id")
	list_filter = ("organization",)


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "branch", "phone_number", "email", "commission_id")
	search_fields = ("name", "branch__name", "commission_id")
	list_filter = ("branch",)

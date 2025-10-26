from django.contrib import admin
from .models import OrganizationLink

# Register your models here.
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

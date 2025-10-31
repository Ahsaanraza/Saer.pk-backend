from django.contrib import admin
from .models import PaxMovement, RegistrationRule, UniversalRegistration

@admin.register(PaxMovement)
class PaxMovementAdmin(admin.ModelAdmin):
    list_display = ("id", "pax_id", "flight_no", "status", "verified_exit", "agent_id", "departure_airport", "arrival_airport", "departure_time", "arrival_time", "created_at")
    search_fields = ("pax_id", "flight_no", "agent_id", "departure_airport", "arrival_airport")
    list_filter = ("status", "verified_exit", "departure_airport", "arrival_airport")


@admin.register(UniversalRegistration)
class UniversalRegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "name", "status", "is_active", "organization_id", "branch_id")
    search_fields = ("id", "name", "email", "contact_no", "organization_id", "branch_id")
    list_filter = ("type", "status", "is_active")

@admin.register(RegistrationRule)
class RegistrationRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "requirement_text", "benefit_text", "city_needed", "service_allowed", "post_available", "created_at", "updated_at")
    search_fields = ("type", "requirement_text", "benefit_text", "city_needed", "service_allowed", "post_available")
    list_filter = ("type", "city_needed")

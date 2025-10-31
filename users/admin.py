from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "type", "commission_id")
	search_fields = ("user__username", "commission_id")

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Lead
from .tasks import sync_lead_to_zoho

@admin.action(description="Sync selected leads to Zoho")
def sync_to_zoho(modeladmin, request, queryset):
    for lead in queryset:
        sync_lead_to_zoho.delay(lead.id)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("email", "status", "zoho_id")
    actions = [sync_to_zoho]
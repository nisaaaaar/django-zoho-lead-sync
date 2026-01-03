from .zoho_client import ZohoClient
from leads.models import Lead
from django.utils.dateparse import parse_datetime
from leads.models import Lead

def map_lead_to_zoho(lead: Lead):
    return {
        "First_Name": lead.first_name,
        "Last_Name": lead.last_name,
        "Email": lead.email,
        "Phone": lead.phone,
        "Lead_Status": lead.status,
    }

def sync_lead(lead: Lead):
    client = ZohoClient()
    payload = map_lead_to_zoho(lead)

    if not lead.zoho_id:
        lead.zoho_id = client.create_lead(payload)
    else:
        client.update_lead(lead.zoho_id, payload)

    lead.save(update_fields=["zoho_id"])

def upsert_lead_from_zoho(zoho_lead):
    lead, _ = Lead.objects.update_or_create(
        zoho_id=zoho_lead["id"],
        defaults={
            "first_name": zoho_lead.get("First_Name", ""),
            "last_name": zoho_lead.get("Last_Name", ""),
            "email": zoho_lead.get("Email", ""),
            "phone": zoho_lead.get("Phone"),
            "status": zoho_lead.get("Lead_Status", "New") or "New",
            "zoho_modified_time": parse_datetime(
                zoho_lead["Modified_Time"]
            ),
        }
    )
    return lead


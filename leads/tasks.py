from celery import shared_task
from .models import Lead
from .services.sync_service import sync_lead

from django.utils.timezone import now
from datetime import timedelta

from .services.sync_service import upsert_lead_from_zoho
from .services.zoho_client import ZohoClient

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=60, retry_kwargs={"max_retries": 5})
def sync_zoho_to_local(self):
    client = ZohoClient()

    # fetch last synced time
    last_sync = (
        Lead.objects.exclude(zoho_modified_time=None)
        .order_by("-zoho_modified_time")
        .values_list("zoho_modified_time", flat=True)
        .first()
    )

    if not last_sync:
        last_sync = now() - timedelta(days=30)

    leads = client.fetch_updated_leads(last_sync)

    for zoho_lead in leads:
        upsert_lead_from_zoho(zoho_lead)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def sync_lead_to_zoho(self, lead_id):
    lead = Lead.objects.get(id=lead_id)
    sync_lead(lead)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead

@csrf_exempt
def zoho_webhook(request):
    payload = json.loads(request.body)
    data = payload["data"][0]

    zoho_id = data["id"]
    lead = Lead.objects.filter(zoho_id=zoho_id).first()

    if lead:
        lead.status = data.get("Lead_Status", lead.status)
        lead.save()

    return JsonResponse({"status": "ok"})
 
from django.contrib import admin
from django.urls import path
from leads.webhooks import zoho_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("webhooks/zoho/", zoho_webhook),
]

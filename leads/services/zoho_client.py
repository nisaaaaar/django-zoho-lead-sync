import os
import requests
from datetime import datetime
class ZohoClient:
    def __init__(self):
        self.api_base = os.getenv("ZOHO_BASE_URL")
        self.accounts_base = os.getenv("ZOHO_ACCOUNTS_URL")
        self._access_token = None
        self._token_generated_at = None


    def _get_access_token(self):
        if self._access_token and self._token_generated_at:
            if (datetime.utcnow() - self._token_generated_at).seconds < 3300:
                return self._access_token

        url = f"{self.accounts_base}/oauth/v2/token"
        params = {
            "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
            "client_id": os.getenv("ZOHO_CLIENT_ID"),
            "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
            "grant_type": "refresh_token",
        }

        r = requests.post(url, params=params)
        r.raise_for_status()

        data = r.json()
        if "access_token" not in data:
            raise Exception(f"Zoho token error: {data}")

        self._access_token = data["access_token"]
        self._token_generated_at = datetime.utcnow()
        return self._access_token


    def _headers(self):
        return {
            "Authorization": f"Zoho-oauthtoken {self._get_access_token()}",
            "Content-Type": "application/json",
        }

    def create_lead(self, payload):
        r = requests.post(
            f"{self.api_base}/crm/v2/Leads",
            json={"data": [payload]},
            headers=self._headers(),
        )

        if r.status_code == 401:
            raise Exception("Zoho 401: invalid/expired token")

        r.raise_for_status()
        return r.json()["data"][0]["details"]["id"]

    def update_lead(self, zoho_id, payload):
        r = requests.put(
            f"{self.api_base}/crm/v2/Leads/{zoho_id}",
            json={"data": [payload]},
            headers=self._headers(),
        )

        if r.status_code == 401:
            raise Exception("Zoho 401: invalid/expired token")

        r.raise_for_status()

    def fetch_updated_leads(self, modified_since):
        res = requests.get(
            f"{self.api_base}/crm/v2/Leads",
            headers=self._headers(),
            params={
                "modified_since": modified_since.isoformat()
            }
        )

        if res.status_code != 200:
            raise Exception(f"Zoho fetch failed: {res.text}")

        return res.json().get("data", [])

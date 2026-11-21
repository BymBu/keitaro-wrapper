import os
import httpx
from typing import Any
from dotenv import load_dotenv

load_dotenv()

KEITARO_API_URL = os.getenv("KEITARO_API_URL", "https://tlgk.host/admin_api/v1")
KEITARO_API_KEY = os.getenv("KEITARO_API_KEY", "")


class KeitaroClient:
    def __init__(self, base_url: str = KEITARO_API_URL, api_key: str = KEITARO_API_KEY):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.Client(
            timeout=30.0,
            headers={"Api-Key": api_key, "Content-Type": "application/json"},
        )

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.base_url}{path}"
        response = self._client.request(method, url, **kwargs)
        if response.status_code >= 400:
            print("KEITARO ERROR:", response.status_code, response.text)
        response.raise_for_status()
        if not response.content:
            return None
        return response.json()

    # --- Чтение ---

    def list_offers(self) -> list[dict]:
        return self._request("GET", "/offers")

    def list_campaigns(self) -> list[dict]:
        return self._request("GET", "/campaigns")

    def list_groups(self, type_: str = "campaigns") -> list[dict]:
        return self._request("GET", f"/groups?type={type_}")

    def list_domains(self) -> list[dict]:
        return self._request("GET", "/domains")

    def list_stream_schemas(self) -> list[dict]:
        return self._request("GET", "/stream_schemas")

    def list_stream_actions(self) -> list[dict]:
        return self._request("GET", "/streams_actions")

    def list_stream_filters(self) -> list[dict]:
        return self._request("GET", "/stream_filters")

    def list_streams(self, campaign_id: int) -> list[dict]:
        return self._request("GET", f"/campaigns/{campaign_id}/streams")

    def get_campaign(self, campaign_id: int) -> dict:
        return self._request("GET", f"/campaigns/{campaign_id}")

    # --- Кампании ---

    def create_campaign(self, payload: dict) -> dict:
        return self._request("POST", "/campaigns", json=payload)

    def update_campaign(self, campaign_id: int, payload: dict) -> dict:
        return self._request("PUT", f"/campaigns/{campaign_id}", json=payload)

    # --- Потоки ---

    def create_stream(self, payload: dict) -> dict:
        return self._request("POST", "/streams", json=payload)

    def update_stream(self, stream_id: int, payload: dict) -> dict:
        return self._request("PUT", f"/streams/{stream_id}", json=payload)

    def delete_stream(self, stream_id: int) -> None:
        return self._request("DELETE", f"/streams/{stream_id}")

    # --- Высокоуровневый метод: кампания + 2 потока ---

    def create_campaign_with_flows(
        self,
        name: str,
        geo: str,
        offer_id: int,
        group_id: int = 10528,
        domain_id: int = 1813,
        traffic_source_id: int = 836,
        google_url: str = "https://google.com",
    ) -> dict:
        campaign_payload = {
            "name": name,
            "alias": name.lower().replace(" ", "_"),
            "group_id": group_id,
            "domain_id": domain_id,
            "type": "position",
            "state": "active",
            "traffic_source_id": traffic_source_id,
        }
        campaign = self.create_campaign(campaign_payload)
        campaign_id = campaign["id"]

        stream1_payload = {
            "campaign_id": campaign_id,
            "type": "forced",
            "name": "Geo -> Google",
            "state": "active",
            "schema": "redirect",
            "action_type": "http",
            "action_options": {"url": google_url},
            "filter_or": False,
            "filters": [
                {
                    "name": "country",
                    "mode": "accept",
                    "payload": [geo.upper()],
                }
            ],
        }
        stream1 = self.create_stream(stream1_payload)

        stream2_payload = {
            "campaign_id": campaign_id,
            "type": "forced",
            "name": "Offer",
            "state": "active",
            "schema": "landings",
            "action_type": "http",
            "action_options": {"url": google_url},
            "filters": [],
            "offers": [
                {"offer_id": offer_id, "share": 100, "state": "active"}
            ],
        }
        stream2 = self.create_stream(stream2_payload)

        return {
            "campaign": campaign,
            "streams": [stream1, stream2],
        }

    def close(self):
        self._client.close()
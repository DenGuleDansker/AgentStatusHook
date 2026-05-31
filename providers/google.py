import requests
from .base import StatusProvider

GEMINI_SERVICE_IDS = [
    "generativelanguage.googleapis.com",
    "Vertex AI",
    "AI Platform",
]

def _map_google_status(availability: str) -> str:
    availability = availability.lower()
    if "available" in availability or "ok" in availability:
        return "operational"
    if "disruption" in availability or "degraded" in availability:
        return "degraded_performance"
    if "outage" in availability:
        return "major_outage"
    return "degraded_performance"


class GoogleProvider(StatusProvider):
    name = "google"
    URL = "https://status.cloud.google.com/incidents.json"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        r.raise_for_status()
        return r.json()

    def normalize(self, raw):
        STATUS_URL = "https://status.cloud.google.com/"

        active_incidents = [
            i for i in raw
            if i.get("end") is None and any(
                s.lower() in str(i.get("affected_products", [])).lower()
                for s in ["generative", "vertex", "ai platform", "gemini"]
            )
        ]

        if active_incidents:
            incident = active_incidents[0]
            status = "major_outage"
            incidents = [{
                "name": incident.get("external_desc", "Ukendt incident"),
                "status": "active",
                "impact": "major",
                "created_at": incident.get("begin", ""),
                "updated_at": incident.get("modified", ""),
            }]
        else:
            status = "operational"
            incidents = []

        return [{
            "provider": self.name,
            "service": "Gemini API",
            "status": status,
            "updated_at": "",
            "link_to_status": STATUS_URL,
            "incidents": incidents,
        }]

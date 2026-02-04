import requests
from .base import StatusProvider
from .utils import map_indicator

class ClaudeProvider(StatusProvider):
    name = "claude"
    URL = "https://status.claude.com/api/v2/summary.json"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        r.raise_for_status()
        return r.json()

    def normalize(self, raw):
        STATUS_URL = "https://status.claude.com/"

        status = raw["status"]
        
        result = {
            "provider": self.name,
            "service": "global",
            "status": map_indicator(status["indicator"]),
            "updated_at": raw["page"]["updated_at"],
            "link_to_status": STATUS_URL, 
            "incidents": []
        }
        
        # Add incidents if any
        for incident in raw.get("incidents", []):
            result["incidents"].append({
                "id": incident["id"],
                "name": incident["name"],
                "status": incident["status"],
                "impact": incident["impact"],
                "created_at": incident["created_at"],
                "updated_at": incident["updated_at"]
            })
        
        return [result]
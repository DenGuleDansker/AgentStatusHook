import requests
from .base import StatusProvider

class ClaudeProvider(StatusProvider):
    name = "claude"
    URL = "https://status.anthropic.com/api/v2/summary.json"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        r.raise_for_status()
        return r.json()

    def normalize(self, raw):
        events = []
        for c in raw["components"]:
            events.append({
                "provider": self.name,
                "service": c["name"],
                "status": c["status"],
                "updated_at": c["updated_at"]
            })
        return events

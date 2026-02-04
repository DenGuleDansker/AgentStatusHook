import requests
from .base import StatusProvider
from .utils import map_indicator

class OpenAIProvider(StatusProvider):
    name = "openai"
    URL = "https://status.openai.com/api/v2/summary.json"

    def fetch(self):
        r = requests.get(self.URL, timeout=10)
        r.raise_for_status()
        return r.json()

    def normalize(self, raw):
        status = raw["status"]

        return [{
            "provider": self.name,
            "service": "global",
            "status": map_indicator(status["indicator"]),
            "updated_at": raw["page"]["updated_at"]
        }]

import requests
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

EMOJI = {
    "operational": "🟢",
    "degraded_performance": "🟡",
    "partial_outage": "🟠",
    "major_outage": "🔴"
}

def send(event):
    emoji = EMOJI.get(event["status"], "⚪")

    msg = (
        f"{emoji} **{event['provider'].upper()}**\n"
        f"Service: `{event['service']}`\n"
        f"Status: **{event['status']}**"
    )

    requests.post(url=DISCORD_WEBHOOK, json={"content": msg})

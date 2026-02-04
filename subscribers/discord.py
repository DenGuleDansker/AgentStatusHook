import os
import requests

# DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1468645283410874621/UoFlzyW7i7NeFQEA3uDUpd9Osjx205wPsvOwYSRwHc3qjQBCGOvYa3X-mpJoLsLBBYfB"

def send(event):
    if not DISCORD_WEBHOOK:
        print("⚠️ DISCORD_WEBHOOK not set – skipping Discord notification")
        return

    emoji = {
        "operational": "🟢",
        "degraded_performance": "🟡",
        "partial_outage": "🟠",
        "major_outage": "🔴"
    }.get(event["status"], "⚪")

    msg = (
        f"{emoji} **{event['provider'].upper()}**\n"
        f"Service: `{event['service']}`\n"
        f"Status: **{event['status']}**"
    )

    requests.post(url=DISCORD_WEBHOOK, json={"content": msg})

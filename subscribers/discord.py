import os
import requests

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

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
    

    # Add incidents if any
    incidents = event.get("incidents", [])
    if incidents:
        msg += "\n\n**🚨 Active Incidents:**"
        for incident in incidents:
            impact_emoji = {
                "none": "🟢",
                "minor": "🟡",
                "major": "🟠",
                "critical": "🔴"
            }.get(incident.get("impact", "").lower(), "⚪")
            
            msg += (
                f"\n{impact_emoji} **{incident['name']}**\n"
                f"  Status: `{incident['status']}`\n"
                f"  Impact: `{incident['impact']}`"
            )
            
            if incident.get("shortlink"):
                msg += f"\n  Link: {incident['shortlink']}"

    requests.post(url=DISCORD_WEBHOOK, json={"content": msg})
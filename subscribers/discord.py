import os
import requests

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send(events):
    if not DISCORD_WEBHOOK:
        print("⚠️ DISCORD_WEBHOOK not set – skipping Discord notification")
        return

    # Gruppér hændelser efter udbyder
    provider_messages = {}

    for event in events:
        emoji = {
            "operational": "🟢",
            "degraded_performance": "🟡",
            "partial_outage": "🟠",
            "major_outage": "🔴"
        }.get(event["status"], "⚪")

        # Opret besked for hver udbyder
        msg = (
            f"{emoji} **{event['provider'].upper()}**\n"
            f"Service: `{event['service']}`\n"
            f"Status: **{event['status']}**\n"
            f"Link to status: **{event['link_to_status']}**"
        )

        # Tilføj hændelser for denne udbyder
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

        # Gem besked for hver udbyder
        provider_messages[event['provider']] = msg

    # Send beskeder for hver udbyder
    for provider, message in provider_messages.items():
        requests.post(url=DISCORD_WEBHOOK, json={"content": message})
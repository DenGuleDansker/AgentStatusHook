import os
import requests

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Global variabel til at holde styr på om live beskeden allerede er sendt
live_message_sent = False

def send(event):
    global live_message_sent
    
    # Hvis live beskeden allerede er sendt, returner med det samme
    if live_message_sent:
        return

    if not DISCORD_WEBHOOK:
        print("⚠️ DISCORD_WEBHOOK not set – skipping Discord notification")
        return

    # Send "Connection er kørende" besked første gang
    msg = "🟢 **Connection er kørende**"
    requests.post(url=DISCORD_WEBHOOK, json={"content": msg})
    
    # Sæt live_message_sent til True efter afsendelse
    live_message_sent = True

    # Resten af din eksisterende logik kan fortsætte her
    emoji = {
        "operational": "🟢",
        "degraded_performance": "🟡",
        "partial_outage": "🟠",
        "major_outage": "🔴"
    }.get(event["status"], "⚪")

    detailed_msg = (
        f"{emoji} **{event['provider'].upper()}**\n"
        f"Service: `{event['service']}`\n"
        f"Status: **{event['status']}**"
    )
    
    # Add incidents if any
    incidents = event.get("incidents", [])
    if incidents:
        detailed_msg += "\n\n**🚨 Active Incidents:**"
        for incident in incidents:
            impact_emoji = {
                "none": "🟢",
                "minor": "🟡",
                "major": "🟠",
                "critical": "🔴"
            }.get(incident.get("impact", "").lower(), "⚪")
            
            detailed_msg += (
                f"\n{impact_emoji} **{incident['name']}**\n"
                f"  Status: `{incident['status']}`\n"
                f"  Impact: `{incident['impact']}`"
            )
            
            if incident.get("shortlink"):
                detailed_msg += f"\n  Link: {incident['shortlink']}"

    # Kommenteret ud, så den ikke sender yderligere beskeder
    # requests.post(url=DISCORD_WEBHOOK, json={"content": detailed_msg})

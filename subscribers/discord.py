import os
import requests
import logging

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send(events):
    if not DISCORD_WEBHOOK:
        logging.warning("⚠️ DISCORD_WEBHOOK not set – skipping Discord notification")
        return

    # Konverter til liste hvis det er en enkelt event
    if isinstance(events, dict):
        events = [events]

    # Gruppér hændelser efter udbyder
    provider_messages = {}

    for event in events:
        # Sikr at event er en dictionary
        if not isinstance(event, dict):
            logging.error(f"Ugyldigt event: {event}")
            continue

        emoji = {
            "operational": "🟢",
            "degraded_performance": "🟡",
            "partial_outage": "🟠",
            "major_outage": "🔴"
        }.get(event.get("status", ""), "⚪")

        # Sikr at nødvendige nøgler eksisterer
        provider = event.get("provider", "Unknown")
        service = event.get("service", "global")
        status = event.get("status", "unknown")
        link_to_status = event.get("link_to_status", "N/A")

        # Opret besked for hver udbyder
        msg = (
            f"{emoji} **{provider.upper()}**\n"
            f"Service: `{service}`\n"
            f"Status: **{status}**\n"
            f"Link to status: **{link_to_status}**"
        )

        # Tilføj hændelser for denne udbyder
        incidents = event.get("incidents", [])
        if incidents:
            msg += "\n\n**🚨 Active Incidents:**"
            for incident in incidents:
                # Sikr at incident er en dictionary
                if not isinstance(incident, dict):
                    logging.error(f"Ugyldigt incident: {incident}")
                    continue

                impact_emoji = {
                    "none": "🟢",
                    "minor": "🟡",
                    "major": "🟠",
                    "critical": "🔴"
                }.get(incident.get("impact", "").lower(), "⚪")
                
                msg += (
                    f"\n{impact_emoji} **{incident.get('name', 'Unknown Incident')}**\n"
                    f"  Status: `{incident.get('status', 'N/A')}`\n"
                    f"  Impact: `{incident.get('impact', 'N/A')}`"
                )
                
                if incident.get("shortlink"):
                    msg += f"\n  Link: {incident['shortlink']}"

        # Gem besked for hver udbyder
        provider_messages[provider] = msg

    # Send beskeder for hver udbyder
    for provider, message in provider_messages.items():
        try:
            requests.post(url=DISCORD_WEBHOOK, json={"content": message})
            logging.info(f"Besked sendt for {provider}")
        except Exception as e:
            logging.error(f"Fejl ved sending af besked for {provider}: {e}")
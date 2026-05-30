import os
import requests
import logging
from datetime import datetime, timezone

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

STATUS_CONFIG = {
    "operational":         {"emoji": "🟢", "color": 0x2ECC71},
    "degraded_performance":{"emoji": "🟡", "color": 0xF1C40F},
    "partial_outage":      {"emoji": "🟠", "color": 0xE67E22},
    "major_outage":        {"emoji": "🔴", "color": 0xE74C3C},
}

IMPACT_EMOJI = {
    "none":     "🟢",
    "minor":    "🟡",
    "major":    "🟠",
    "critical": "🔴",
}

def _fmt_time(raw: str) -> str:
    if not raw:
        return "N/A"
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y %H:%M UTC")
    except ValueError:
        return raw


def _build_embed(event: dict) -> dict:
    status = event.get("status", "unknown")
    cfg = STATUS_CONFIG.get(status, {"emoji": "⚪", "color": 0x95A5A6})

    provider   = event.get("provider", "Unknown")
    service    = event.get("service", "global")
    link       = event.get("link_to_status") or ""
    updated_at = _fmt_time(event.get("updated_at", ""))

    title = f"{cfg['emoji']} {provider.upper()} — {status.replace('_', ' ').title()}"

    fields = [
        {"name": "Service",      "value": f"`{service}`",    "inline": True},
        {"name": "Status",       "value": f"`{status}`",     "inline": True},
        {"name": "Opdateret",    "value": f"`{updated_at}`", "inline": True},
    ]

    if link:
        fields.append({"name": "Status page", "value": f"[{provider} status]({link})", "inline": False})

    incidents = event.get("incidents", [])
    for incident in incidents:
        if not isinstance(incident, dict):
            continue
        impact      = incident.get("impact", "").lower()
        ie          = IMPACT_EMOJI.get(impact, "⚪")
        name        = incident.get("name", "Unknown Incident")
        istat       = incident.get("status", "N/A")
        ilink       = incident.get("shortlink", "")
        created_at  = _fmt_time(incident.get("created_at", ""))
        iupdated_at = _fmt_time(incident.get("updated_at", ""))

        value = (
            f"Status: `{istat}` · Impact: `{impact}`\n"
            f"Startet: `{created_at}`\n"
            f"Sidst opdateret: `{iupdated_at}`"
        )
        if ilink:
            value += f"\n[View incident]({ilink})"
        fields.append({"name": f"{ie} {name}", "value": value, "inline": False})

    return {
        "title": title,
        "color": cfg["color"],
        "fields": fields,
        "footer": {"text": "Agent Status Monitor"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def send(events):
    if not DISCORD_WEBHOOK:
        logging.warning("DISCORD_WEBHOOK not set – skipping Discord notification")
        return

    if isinstance(events, dict):
        events = [events]

    for event in events:
        if not isinstance(event, dict):
            logging.error(f"Invalid event: {event}")
            continue

        embed = _build_embed(event)
        try:
            resp = requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]})
            resp.raise_for_status()
            logging.info(f"Discord embed sent for {event.get('provider', '?')}")
        except Exception as e:
            logging.error(f"Failed to send Discord embed for {event.get('provider', '?')}: {e}")

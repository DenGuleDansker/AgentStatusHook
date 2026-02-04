def map_indicator(indicator: str) -> str:
    return {
        "none": "operational",
        "minor": "degraded",
        "major": "outage",
        "critical": "outage"
    }.get(indicator, "unknown")
